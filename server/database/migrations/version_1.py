import aiosqlite

import logging


logger = logging.getLogger("MIGRATION_1")


class Migration:
    version = 1

    async def run(self, connection: aiosqlite.Connection):
        logger.debug("RUNNING MIGRATION 1")
        await connection.execute(
            "CREATE TABLE Users("
            "   id INTEGER PRIMARY KEY,"
            "   name TEXT NOT NULL UNIQUE,"
            "   password TEXT NOT NULL"
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
            "   owner_id INTEGER NOT NULL,"
            "   path TEXT NOT NULL,"
            "   filename TEXT NOT NULL,"
            "   uploaded INTEGER NOT NULL,"
            "   folder_id INTEGER NOT NULL"
            ")"
        )

        await connection.execute(
            "CREATE TABLE Options("
            "   id INTEGER PRIMARY KEY,"
            "   key TEXT NOT NULL UNIQUE,"
            "   value TEXT NOT NULL"
            ")"
        )
