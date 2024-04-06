from pydantic import BaseModel


class RepoSchema(BaseModel):
    repo: str
    owner: str
    position_cur: int
    position_prev: int | None
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str | None
