import fastapi
import logging
import json
from fastapi.security import OAuth2PasswordRequestForm
from time import time
from typing import Optional

from server.database import db
from server.database.models.users import User
from server.database.models.files import File
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