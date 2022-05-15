import aiosqlite
import pytest
import httpx

from server.database.migrations import run_migrations
from server.api import API_app
from server.database import db


@pytest.fixture()
async def db_override():
    async with aiosqlite.connect(":memory:") as db:
        await run_migrations(db)
        yield db


@pytest.fixture()
async def client(db_override):
    async def get_db():
        yield db_override

    API_app.dependency_overrides[db] = get_db
    async with httpx.AsyncClient(app=API_app, base_url="http://localhost") as client:
        yield client


@pytest.mark.asyncio
async def test_register_route(client):
    response = await client.post(
        "/register",
        data={
            "username": "Bob",
            "password": "SECRET"
        }
    )
    assert response.status_code == 200
    assert response.json()["user-id"] == 1


@pytest.mark.asyncio
async def test_login_route(client):
    await client.post("/register", data={"username": "Bob", "password": "SECRET"})
    response = await client.post("/login", data={"username": "Bob", "password": "SECRET"})
    assert response.status_code == 200
    assert len(response.json()["token"]) == 32
