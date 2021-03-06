from __future__ import annotations
from aiosqlite import Connection
from server.database.models import BaseModel
from time import time


class Session(BaseModel):
    token: str
    data: str
    expires: int

    db: Connection

    async def refresh(self, db: Connection):
        await db.execute(
            "UPDATE Sessions"
            "   SET expires=?"
            " WHERE token == ?", (int(time()) + 600, self.token)
        )
        await db.commit()

    @classmethod
    async def create(cls, token: str, data: str, expires: int, db: Connection):
        await db.execute(
            "INSERT INTO Sessions(token, data, expires)"
            "     VALUES(?, ?, ?)",
            (token, data, expires)
        )
        await db.commit()

    @classmethod
    async def get(cls, token: str, db: Connection) -> Session:
        async with db.execute("SELECT * FROM Sessions WHERE token == ?", (token,)) as cursor:
            row = await cursor.fetchone()
            return cls._create_session(row, db)

    @classmethod
    def _create_session(cls, row, db) -> Session:
        fields = dict(item for item in zip(["token", "data", "expires"], row))
        return Session(**fields, db=db)
