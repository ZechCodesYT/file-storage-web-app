import aiosqlite

import logging


logger = logging.getLogger("MIGRATION_2")


class Migration:
    version = 2

    async def run(self, connection: aiosqlite.Connection):
        logger.debug("RUNNING MIGRATION 2")
        await connection.execute(
            "CREATE TABLE Sessions("
            "   token TEXT(32) PRIMARY KEY,"
            "   data TEXT NOT NULL,"
            "   expires INTEGER NOT NULL"
            ")"
        )
