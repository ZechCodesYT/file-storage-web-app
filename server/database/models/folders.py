from __future__ import annotations
from aiosqlite import Connection
from server.database.models.users import User
from server.database.models import BaseModel
from pydantic import Field


class Folder(BaseModel):
    id: int
    name: str
    parent_id: int
    owner_id: int

    db: Connection = Field(export=False)

    @property
    async def parent(self) -> Folder | None:
        if self.parent_id == -1:
            return None

        return await Folder.get(self.parent_id, self.db)

    @property
    async def owner(self) -> User:
        return await User.get(self.owner_id, self.db)

    @classmethod
    async def create(cls, name: str, parent_id: int, owner_id: int, db: Connection) -> Folder:
        cursor = await db.execute(
            "INSERT INTO Folders(name, parent_id, owner_id)"
            "     VALUES(?, ?, ?)",
            (name, parent_id, owner_id)
        )
        await db.commit()
        return await cls.get(cursor.lastrowid, owner_id, db)

    @classmethod
    async def get(cls, folder_id: int, user_id: int, db: Connection) -> Folder:
        if folder_id == -1:
            return Folder(id=-1, name="root", parent_id=-1, owner_id=user_id, db=db)

        async with db.execute("SELECT * FROM Folders WHERE id == ? AND owner_id == ?", (folder_id, user_id)) as cursor:
            row = await cursor.fetchone()
            fields = dict(item for item in zip(["id", "name", "parent_id", "owner_id"], row))
            return Folder(**fields, db=db)

    @classmethod
    async def get_folders(cls, parent_id: int, user_id: int, db: Connection) -> list[Folder]:
        async with db.execute("SELECT * FROM Folders WHERE parent_id == ? AND owner_id == ?", (parent_id, user_id)) as cursor:
            rows = await cursor.fetchall()
            return [cls.create_model(row, db) for row in rows]

    @classmethod
    def create_model(cls, row, db) -> Folder:
        fields = dict(item for item in zip(["id", "name", "parent_id", "owner_id"], row))
        return Folder(**fields, db=db)
