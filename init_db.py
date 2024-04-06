import os
import asyncpg
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def initialize_db():
    try:
        conn = await asyncpg.connect(database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'),
                                     port=os.getenv('DB_PORT'), host=os.getenv('DB_HOSTNAME'),
                                     password=os.getenv('DB_PASSWORD'))
    except Exception as e:
        print(f'Ошибка подключения к БД: {e!r}')
        return

    async with conn.transaction():
        try:
            await conn.execute(
                """create table repos (
                id serial,
                repo varchar primary key not null unique,
                owner varchar not null,
                stars integer not null,
                watchers integer not null,
                forks integer not null,
                open_issues integer not null,
                position_cur integer not null,
                position_prev integer default null,
                language varchar);"""
            )
        except Exception as e:
            print(f'Не удалось создать таблицу repos: {e!r}')

        try:
            await conn.execute(
                """create table commits (
                    id serial primary key,
                    date timestamp without time zone not null,
                    author varchar not null,
                    repo_name varchar not null,
                    constraint fk_repo foreign key(repo_name) references repos(repo),
                    constraint ux_author_date UNIQUE (author, date)
                    );"""
            )
        except Exception as e:
            print(f'Не удалось создать таблицу commits: {e!r}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_db())
