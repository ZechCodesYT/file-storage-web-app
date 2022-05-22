import fastapi
import logging
import json
from fastapi.security import OAuth2PasswordRequestForm
from time import time
from typing import Optional

from server.database import db
from server.database.models.files import File
from server.database.models.folders import Folder
from server.database.models.sessions import Session
from server.database.models.users import User
from server.auth import hash_password, check_password_matches
from server.sessions import create_token, get_session


API_app = fastapi.FastAPI()
logger = logging.getLogger("Server")


@API_app.post("/register")
async def register_user(form_data: OAuth2PasswordRequestForm = fastapi.Depends(), conn=fastapi.Depends(db)):
    await User.create(form_data.username, hash_password(form_data.password), conn)
    user = await User.get_by("name", form_data.username, conn)
    await conn.commit()
    return {"message": "SUCCESS", "user-id": user[0].id}


@API_app.post("/upload")
async def upload(
    file: fastapi.UploadFile,
    filename: Optional[str] = None,
    folder_id: int = -1,
    session=fastapi.Depends(get_session),
    conn=fastapi.Depends(db)
):
    name = filename or file.filename

    path = await File.save_to_disk(file, session["user-id"])
    model = await File.create(path, name, int(time()), session["user-id"], folder_id, conn)
    return {
        "file_id": model.id
    }


@API_app.post("/create-folder")
async def create_folder(
    name: str,
    parent_id: int,
    session=fastapi.Depends(get_session),
    conn=fastapi.Depends(db)
):
    folder = await Folder.create(name, parent_id, session["user-id"], conn)
    return {
        "folder_id": folder.id
    }


@API_app.get("/list/{folder_id}")
async def list_files(folder_id: int, conn=fastapi.Depends(db), session=fastapi.Depends(get_session)):
    return {
        "files": await File.get_files(folder_id, session["user-id"], conn),
        "folders": await Folder.get_folders(folder_id, session["user-id"], conn)
    }


@API_app.get("/file/{file_id}")
async def download_file(file_id: int, conn=fastapi.Depends(db), session=fastapi.Depends(get_session)):
    file = await File.get(file_id, session["user-id"], conn)
    if not file:
        raise fastapi.HTTPException(404, {"status": "FAILED", "message": f"File does not exist"})

    return fastapi.responses.FileResponse(file.path, filename=file.filename)


@API_app.delete("/file/{file_id}")
async def delete_file(file_id: int, conn=fastapi.Depends(db), session=fastapi.Depends(get_session)):
    await File.delete(file_id, session["user-id"], conn)
    return {"status": "success"}


@API_app.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = fastapi.Depends(), conn=fastapi.Depends(db)):
    user = await User.get_by("name", form_data.username, conn)
    if not user or not check_password_matches(form_data.password, user[0].password):
        logger.info("LOGIN FAILED")
        raise fastapi.HTTPException(401, {"status": "FAILED", "message": f"User's name or password was incorrect. {user!r}"})

    logger.info("LOGIN SUCCEEDED")
    token = create_token()
    await Session.create(token, json.dumps({"user-id": user[0].id}), int(time()) + 600, conn)
    return {"access_token": token, "token_type": "bearer"}