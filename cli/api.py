from __future__ import annotations
from io import BytesIO
from typing import Any
from contextlib import suppress
import pathlib

import httpx
import pydantic
import typer


class APIWrapper:
    def __init__(
        self,
        host: str = "http://localhost:8000",
        auth_file: pathlib.Path = pathlib.Path("~/.file-sync-token.secret").expanduser()
    ):
        self.host = host
        self.auth_token = self._load_authorization(auth_file)
        self.auth_file = auth_file

    @property
    def connection(self):
        params = {}
        if self.auth_token:
            params["headers"] = {"Authorization": f"bearer {self.auth_token}"}
        return httpx.AsyncClient(base_url=self.host.rstrip('/'), **params)

    async def _request(
        self,
        method: str,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        files: list[BytesIO] | None = None,
        data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        async with self.connection as client:
            params = {}
            if data:
                params["data"] = data
            if payload:
                params["json"] = payload
                params["headers"] = {"Content-Type": "application/json"}
            response = await client.request(method, f"/api/v1/{endpoint.lstrip('/')}", **params)
            return response.json()

    async def create_folder(self, name: str, parent_id: int) -> Folder:
        data = await self._request("POST", "/create-folder", payload={"name": name, "parent_id": parent_id})
        if "folder_id" in data:
            return await self.get_folder(data["folder_id"])
        else:
            typer.secho(f"There was a problem while attempting to create the folder {name}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    async def get_folder(self, id: int) -> Folder:
        data = await self._request("GET", f"/list/{int(id)}")
        files = [File.create(**file, api=self) for file in data["files"]]
        folders = [Folder.create(**folder, api=self) for folder in data["folders"]]
        return Folder.create(**data["folder"], files=files, folders=folders, api=self)

    async def login(self, username: str, password: str) -> bool:
        with suppress(Exception):
            response = await self._request("POST", "/login", data={"username": username, "password": password})
            if "access_token" in response:
                self._save_auth_token(response["access_token"])
            return True

        return False

    async def register(self, username: str, password: str) -> int | None:
        with suppress(Exception):
            data = await self._request("POST", "/register", data={"username": username, "password": password})

            if data.get("message") == "SUCCESS":
                return data["user-id"]

        return None

    def _save_auth_token(self, token: str):
        with self.auth_file.open("w") as file:
            file.write(token)

    def _load_authorization(self, auth_file: pathlib.Path) -> str | None:
        try:
            file = auth_file.open("r")
        except FileNotFoundError:
            return None
        else:
            with file:
                return file.read()


class BaseModel(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True


class User(BaseModel):
    id: int
    name: str
    api: APIWrapper = pydantic.Field(default=None)

    @classmethod
    def create(cls, id: str, name: str, api: APIWrapper) -> User:
        user = User(id=id, name=name)
        user.api = api
        return user


class File(BaseModel):
    id: int
    path: str  # Path to the file on disk
    filename: str
    uploaded: int
    owner_id: int
    folder_id: int
    api: APIWrapper = pydantic.Field(default=None)

    @property
    async def parent(self) -> Folder | None:
        if self.parent_id == -1:
            return None

        return await Folder.get(self.parent_id, self.db)

    @property
    async def owner(self) -> User:
        return await User.get(self.owner_id, self.db)

    @classmethod
    def create(
        cls, id: str, path: str, filename: str, uploaded: int, owner_id: int, folder_id: int, api: APIWrapper
    ) -> File:
        file = File(id=id, path=path, uploaded=uploaded, owner_id=owner_id, folder_id=folder_id)
        file.api = api
        return file


class Folder(BaseModel):
    id: int
    name: str
    parent_id: int
    owner_id: int
    files: list[File] = pydantic.Field(default_factory=list)
    folders: list[Folder] = pydantic.Field(default_factory=list)
    api: APIWrapper = pydantic.Field(default=None)

    @property
    async def parent(self) -> Folder | None:
        if self.parent_id == -1:
            return None

        return await Folder.get(self.parent_id, self.db)

    @property
    async def owner(self) -> User:
        return await User.get(self.owner_id, self.db)

    @classmethod
    def create(
        cls,
        id: str,
        name: str,
        parent_id: int,
        owner_id: int,
        api: APIWrapper,
        files: list[File] | None = None,
        folders: list[Folder] | None = None
    ) -> Folder:
        folder = Folder(
            id=id, name=name, parent_id=parent_id, owner_id=owner_id, files=files or [], folders=folders or []
        )
        folder.api = api
        return folder
