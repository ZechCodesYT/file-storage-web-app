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

    typer.secho(f"Syncing {local_folder} to {folder_name}", fg=typer.colors.GREEN)


def _create_folder(name: str, parent_id: int) -> Folder:
    api = APIWrapper()
    return asyncio.run(api.create_folder(name, parent_id))


def _find_folder_in_folder_by_name(name: str, folder: Folder) -> Folder | None:
    for _folder in folder.folders:
        if _folder.name == name:
            return _folder

    return None
