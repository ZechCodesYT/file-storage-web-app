from __future__ import annotations
from aiosqlite import Connection
from server.database.models.folders import Folder
from server.database.models.users import User
from server.database.models import BaseModel


class File(BaseModel):
    id: int
    path: str
    filename: str
    uploaded: int
    owner_id: int
    folder_id: int

    db: Connection

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
        await db.execute(
            "INSERT INTO Files(path, filename, uploaded, owner_id, folder_id)"
            "     VALUES(?, ?, ?, ?, ?)",
            (path, filename, uploaded, owner_id, folder_id)
        )

    @classmethod
    async def get(cls, file_id: int, db: Connection) -> File:
        async with db.execute("SELECT * FROM Files WHERE id == ?", (file_id,)) as cursor:
            row = await cursor.fetchone()
            fields = dict(item for item in zip(["id", "path", "filename", "uploaded", "owner_id", "folder_id"], row))
            return File(**fields, db=db)
