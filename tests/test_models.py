import aiosqlite
import pytest

from server.database.migrations import version_1
from server.database.models.files import File
from server.database.models.folders import Folder
from server.database.models.users import User


@pytest.fixture()
async def db():
    async with aiosqlite.connect(":memory:") as db:
        migration = version_1.Migration()
        await migration.run(db)
        yield db


@pytest.fixture(autouse=True)
async def create_user(db):
    await db.execute("INSERT INTO Users VALUES (0, 'Bob', 'SECRET')")


@pytest.fixture(autouse=True)
async def create_folder(db):
    await db.execute("INSERT INTO Folders VALUES (0, 'My Folder', -1, 0)")


@pytest.fixture(autouse=True)
async def create_file(db):
    await db.execute("INSERT INTO Files VALUES (0, 0, 'files/taohusnehusna.png', 'My PNG.png', 23456789876, 0)")


@pytest.mark.asyncio
async def test_file_model(db):
    file = await File.get(0, db)
    assert file.filename == "My PNG.png"
    assert (await file.owner).name == "Bob"
    assert (await file.folder).name == "My Folder"


@pytest.mark.asyncio
async def test_folder_model(db):
    folder = await Folder.get(0, db)
    assert folder.name == "My Folder"
    assert (await folder.owner).name == "Bob"


@pytest.mark.asyncio
async def test_user_model(db):
    user = await User.get(0, db)
    assert user.name == "Bob"
