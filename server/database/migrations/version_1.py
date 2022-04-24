import aiosqlite


class Migration:
    version = 1

    async def run(self, connection: aiosqlite.Connection):
        await connection.execute(
            "CREATE TABLE Users("
            "   id INTEGER PRIMARY KEY,"
            "   name TEXT NOT NULL UNIQUE,"
            "   passwords TEXT NOT NULL"
            ")"
        )

        await connection.execute(
            "CREATE TABLE Folders("
            "   id INTEGER PRIMARY KEY,"
            "   name TEXT NOT NULL,"
            "   parent_id INTEGER NOT NULL,"
            "   owner_id INTEGER NOT NULL"
            ")"
        )

        await connection.execute(
            "CREATE TABLE Files("
            "   id INTEGER PRIMARY KEY,"
            "   name TEXT NOT NULL,"
            "   owner_id INTEGER NOT NULL,"
            "   path TEXT NOT NULL,"
            "   filename TEXT NOT NULL,"
            "   uploaded INTEGER NOT NULL,"
            "   folder_id INTEGER NOT NULL"
            ")"
        )
