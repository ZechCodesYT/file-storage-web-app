import aiosqlite
import pytest

from server.database.migrations import version_1


@pytest.mark.asyncio
async def test_migration_version_1():
    async with aiosqlite.connect(":memory:") as db:
        migration = version_1.Migration()
        await migration.run(db)

        tables_result = db.execute("SELECT name FROM sqlite_master WHERE type='table';")
        async with tables_result as cursor:
            table_names = await cursor.fetchall()

        assert {row[0] for row in table_names} == {"Users", "Folders", "Files"}
