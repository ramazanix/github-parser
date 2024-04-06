from fastapi import APIRouter, Depends, Query
from typing import Annotated
from asyncpg import Pool
from src.schemas.top_repos import RepoSchema
from src.schemas.repo_activity import RepoActivitySchema
from src.db import get_db
from datetime import date

repos_router = APIRouter(prefix='/repos', tags=['Repos'])


@repos_router.get('/top100', response_model=list[RepoSchema])
async def get_top100(db: Annotated[Pool, Depends(get_db)], sort_by: str | None = 'stars', order: str | None = 'desc'):
    sort_presented = sort_by in (
        'repo', 'owner', 'position_prev', 'position_prev', 'watchers', 'forks', 'open_issues', 'language', 'stars'
    )
    order_presented = order in ('desc', 'asc')

    if not sort_presented:
        sort_by = 'stars'

    if not order_presented:
        order = 'desc'

    query = '''select * from repos order by {} {};'''.format(sort_by, order)

    async with db.acquire() as conn:
        result = await conn.fetch(query)

    result = list(map(dict, result))
    return result


@repos_router.get('/{owner}/{repo}/activity', response_model=list[RepoActivitySchema])
async def get_repo_activity(owner: str, repo: str, db: Annotated[Pool, Depends(get_db)],
                            since: Annotated[date | None, Query()], until: Annotated[date | None, Query()]):
    repo_name = '/'.join((owner, repo))

    query = '''select date_trunc('day', date) as date, count(*) as commits, array_agg(distinct author) as authors 
               from commits where date between $1 and $2 and repo_name = $3 
               group by date_trunc('day', date)'''

    async with db.acquire() as conn:
        result = await conn.fetch(query, since, until, repo_name)

    result = list(map(dict, result))
    return result
