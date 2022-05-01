from __future__ import annotations
from aiosqlite import Connection
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    password: str

    db: Connection

    @classmethod
    async def create(cls, name: str, password: str, db: Connection):
        await db.execute(
            "INSERT INTO Users(name, password)"
            "     VALUES(?, ?)",
            (name, password)
        )

    @classmethod
    async def get(cls, user_id: int, db: Connection) -> User:
        async with db.execute("SELECT * FROM Users WHERE id == ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return User(*row, db)
