import aiohttp
import asyncpg
import os
from dateutil import parser
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
    "X-GitHub-Api-Version": "2022-11-28",
    "Accept": "application/vnd.github+json",
}


async def insert_into_table(repo_data):
    try:
        conn = await asyncpg.connect(database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'),
                                     port=os.getenv('DB_PORT'), host=os.getenv('DB_HOSTNAME'),
                                     password=os.getenv('DB_PASSWORD'))
    except Exception as e:
        print(f'Ошибка подключения к БД: {e!r}')
        raise e

    async with conn.transaction():
        try:
            await conn.execute(
                '''insert into repos (repo, owner, stars, watchers, forks, open_issues, language, position_cur) 
                values ($1, $2, $3, $4, $5, $6, $7, $8)
                on conflict (repo) do update set
                owner = excluded.owner, stars = excluded.stars, watchers = excluded.watchers,
                forks = excluded.forks, open_issues = excluded.open_issues, language = excluded.language,
                position_prev = repos.position_cur, position_cur = excluded.position_cur;''',
                repo_data['repo'], repo_data['owner'], repo_data['stars'], repo_data['watchers'],
                repo_data['forks'], repo_data['open_issues'], repo_data['language'], repo_data['pos_cur'])

        except Exception as e:
            print(f'Не удалось вставить/обновить данные в таблице repos: {e!r}')
            raise e

        try:
            await conn.executemany(
                '''insert into commits (author, date, repo_name) values ($1, $2, $3) 
                on conflict (author, date) do nothing;''',
                repo_data['commits'])

        except Exception as e:
            print(f'Не удалось вставить данные в таблицу repos: {e!r}')
            raise e


async def parse_public_repos():
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                    "https://api.github.com/search/repositories?q=is:public+stars:>=50000&sort=stars&per_page=100"
            ) as response:
                data = await response.json()

            for idx, repo in enumerate(data['items']):
                print(f'Parsing commits for repo {repo["name"]}')
                page_items = 100
                page = 1
                repo_commits_info = []

                while page_items == 100 and page < 3:
                    async with session.get(
                            f'https://api.github.com/repos/{repo["full_name"]}/commits?per_page=100&page={page}') as response:
                        commits_data_page = await response.json()

                        for c_idx, commit in enumerate(commits_data_page):
                            repo_commits_info.append(
                                (commit['commit']['author']['name'],
                                 parser.parse(commit['commit']['author']['date'][:-1]),
                                 repo['full_name']))

                        page_items = len(commits_data_page)
                        if page_items == 100:
                            page += 1

                repo_data = {'repo': repo['full_name'], 'owner': repo['owner']['login'],
                             'stars': repo['stargazers_count'], 'watchers': repo['watchers_count'],
                             'forks': repo['forks_count'], 'open_issues': repo['open_issues_count'],
                             'language': repo['language'], 'commits': repo_commits_info, 'pos_cur': idx + 1}

                await insert_into_table(repo_data)
                print(f'Info about repo {repo["name"]} and it commits in table (ID={idx + 1})\n')

    except Exception as e:
        print(f'Error occurred: {e!r}')
        raise e


async def handler(event, context):
    if not (os.getenv('GH_TOKEN') and os.getenv('DB_NAME') and os.getenv('DB_USER') and os.getenv(
            'DB_PASSWORD') and os.getenv('DB_HOSTNAME') and os.getenv('DB_PORT')):
        raise Exception('Provide env variables')

    await parse_public_repos()
