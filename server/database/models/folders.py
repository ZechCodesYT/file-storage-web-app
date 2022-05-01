from __future__ import annotations
from dataclasses import dataclass
from aiosqlite import Connection
from server.database.models.users import User


@dataclass
class Folder:
    id: int
    name: str
    parent_id: int
    owner_id: int

    db: Connection

    @property
    async def parent(self) -> Folder | None:
        if self.parent_id == -1:
            return None

        return await Folder.get(self.parent_id, self.db)

    @property
    async def owner(self) -> User:
        return await User.get(self.owner_id, self.db)

    @classmethod
    async def get(cls, folder_id: int, db: Connection) -> Folder:
        async with db.execute("SELECT * FROM Folders WHERE id == ?", (folder_id,)) as cursor:
            row = await cursor.fetchone()
            return Folder(*row, db)
