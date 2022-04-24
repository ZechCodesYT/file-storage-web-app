import ast
import logging
from typing import Any

logger = logging.getLogger("DB")
logger.setLevel(logging.DEBUG)


async def get_option(name: str, db) -> Any:
    async with db.execute("SELECT value FROM Options WHERE key == ?", (name,)) as cursor:
        row = await cursor.fetchone()
        logger.debug(f"Row: {row}")
        return ast.literal_eval(row[0])


async def set_option(name: str, value: Any, db):
    logger.debug(f"Setting {name} to {value!r}")
    async with db.execute("REPLACE INTO Options(key, value) VALUES(?, ?);", (name, repr(value))) as cursor:
        await db.commit()
