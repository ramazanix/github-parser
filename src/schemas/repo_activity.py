from pydantic import BaseModel
from datetime import date


class RepoActivitySchema(BaseModel):
    date: date
    commits: int
    authors: list[str]
