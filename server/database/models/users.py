from __future__ import annotations
from aiosqlite import Connection
from server.database.models import BaseModel


class User(BaseModel):
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
    async def get_by(cls, field: str, value: str, db: Connection) -> list[User]:
        if not field.isalnum():
            raise Exception("Field names can only be alpha-numeric")

        async with db.execute(f"SELECT * FROM Users WHERE {field} == ?", ( value,)) as cursor:
            rows = await cursor.fetchall()
            return [cls._create_user(row, db=db) for row in rows]

    @classmethod
    async def get(cls, user_id: int, db: Connection) -> User:
        async with db.execute("SELECT * FROM Users WHERE id == ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return cls._create_user(row, db)

    @classmethod
    def _create_user(cls, row, db) -> User:
        fields = dict(item for item in zip(["id", "name", "password"], row))
        return User(**fields, db=db)