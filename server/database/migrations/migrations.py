import sqlite3
import importlib
from typing import Protocol

from server.database.options import get_option, set_option


class MigrationProtocol(Protocol):
    version: int

    async def run(self, connection):
        ...


def get_available_migrations_after(version: int) -> list[MigrationProtocol]:
    migrations = []
    while True:
        version += 1
        try:
            migration_module = importlib.import_module(f"server.database.migrations.version_{version}")
        except ImportError:
            break
        else:
            migrations.append(migration_module.Migration())

    return migrations


async def get_database_version(db) -> int:
    try:
        return await get_option("db-version", db)
    except sqlite3.OperationalError:
        return 0


async def run_migrations(db):
    version = await get_database_version(db)
    new_version = await run_migrations_from(version, db)
    if new_version != version:
        await set_option("db-version", new_version, db)


async def run_migrations_from(version, db) -> int:
    migrations = get_available_migrations_after(version)
    if not migrations:
        return version

    for migration in migrations:
        await migration.run(db)

    return migration.version
