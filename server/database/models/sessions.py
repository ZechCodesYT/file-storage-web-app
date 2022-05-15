from __future__ import annotations
from aiosqlite import Connection
from server.database.models import BaseModel


class Session(BaseModel):
    id: int
    data: str
    expires: int

    db: Connection

    @classmethod
    async def create(cls, token: str, data: str, expires: int, db: Connection):
        await db.execute(
            "INSERT INTO Sessions(token, data, expires)"
            "     VALUES(?, ?, ?)",
            (token, data, expires)
        )

    @classmethod
    async def get(cls, token: str, db: Connection) -> Session:
        async with db.execute("SELECT * FROM Sessions WHERE token == ?", (token,)) as cursor:
            row = await cursor.fetchone()
            return cls._create_session(row, db)

    @classmethod
    def _create_session(cls, row, db) -> Session:
        fields = dict(item for item in zip(["token", "data", "expires"], row))
        return Session(**fields, db=db)
