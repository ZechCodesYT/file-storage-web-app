from __future__ import annotations
from aiosqlite import Connection
from server.database.models.folders import Folder
from server.database.models.users import User
from server.database.models import BaseModel
from pydantic import Field


class File(BaseModel):
    id: int
    path: str  # Path to the file on disk
    filename: str
    uploaded: int
    owner_id: int
    folder_id: int

    db: Connection = Field(export=False)

    @property
    async def folder(self) -> Folder | None:
        if self.folder_id == -1:
            return None

        return await Folder.get(self.folder_id, self.db)

    @property
    async def owner(self) -> User:
        return await User.get(self.owner_id, self.db)

    @classmethod
    async def create(cls, path: str, filename: str, uploaded: int, owner_id: int, folder_id: int, db: Connection):
        cursor = await db.execute(
            "INSERT INTO Files(path, filename, uploaded, owner_id, folder_id)"
            "     VALUES(?, ?, ?, ?, ?)",
            (path, filename, uploaded, owner_id, folder_id)
        )
        await db.commit()
        return await cls.get(cursor.lastrowid, owner_id, db)

    @classmethod
    async def get(cls, file_id: int, db: Connection) -> File:
        async with db.execute("SELECT * FROM Files WHERE id == ?", (file_id,)) as cursor:
            row = await cursor.fetchone()
            fields = dict(item for item in zip(["id", "path", "filename", "uploaded", "owner_id", "folder_id"], row))
            return File(**fields, db=db)

    @classmethod
    async def get_files(cls, folder_id: int, user_id: int, db: Connection) -> list[File]:
        async with db.execute("SELECT * FROM Files WHERE folder_id == ? AND owner_id == ?", (folder_id, user_id)) as cursor:
            rows = await cursor.fetchall()
            return [cls.create_file_model(row, db) for row in rows]

    @classmethod
    def create_file_model(cls, row, db) -> File:
        fields = dict(item for item in zip(["id", "path", "filename", "uploaded", "owner_id", "folder_id"], row))
        return File(**fields, db=db)
