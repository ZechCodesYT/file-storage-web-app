from __future__ import annotations
import pathlib
import typer
import asyncio
from cli.api import APIWrapper, Folder


def sync_folder(folder_name: str, local_folder: pathlib.Path):
    root = asyncio.run(APIWrapper().get_folder(-1))
    folder = _find_folder_in_folder_by_name(folder_name, root)
    if not folder:
        typer.secho(f"Folder {folder_name} not found, creating.")
        folder = _create_folder(folder_name, -1)

    folder = asyncio.run(APIWrapper().get_folder(folder.id))
    typer.secho(f"Syncing {local_folder} to {folder_name}", fg=typer.colors.GREEN)
    asyncio.run(_do_folder_sync(local_folder, folder))


def _create_folder(name: str, parent_id: int) -> Folder:
    api = APIWrapper()
    return asyncio.run(api.create_folder(name, parent_id))


async def _do_folder_sync(local_folder: pathlib.Path, folder: Folder, api: APIWrapper | None = None):
    api = api or APIWrapper()
    new_folders = []
    for f in local_folder.iterdir():
        if f.is_dir() and not _find_folder_in_folder_by_name(f.name, folder) and not f.name.startswith((".", "_")):
            new_folders.append(await api.create_folder(f.name, folder.id))

    # Todo: Upload missing files to the server
    # Todo: Recursively upload files in sub-folders
    # Todo: Ignore files that haven't changed
    # Todo: Download missing folders recursively
    # Todo: Download missing files


def _find_folder_in_folder_by_name(name: str, folder: Folder) -> Folder | None:
    for _folder in folder.folders:
        if _folder.name == name:
            return _folder

    return None
