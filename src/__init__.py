from fastapi import FastAPI
from src.config import settings


def init_app(*args):
    server = FastAPI(
        title="GitHub Parser",
    )

    from src.router import repos_router

    server.include_router(repos_router)

    return server
