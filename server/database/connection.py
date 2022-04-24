from __future__ import annotations
import aiosqlite
import logging
from typing import Union

import server.config


logger = logging.getLogger("DB")


async def db(connection: Union[str, None] = None):
    db_file = connection or server.config.get_config()["db-connection"]
    logger.debug(f"Opening {db_file}")
    async with aiosqlite.connect(db_file) as session:
        yield session