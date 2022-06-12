from cli.api import APIWrapper
from asyncio import run


def register(username: str, password: str):
    api = APIWrapper()
    return run(api.register(username, password))


def login(username: str, password: str):
    api = APIWrapper()
    run(api.login(username, password))