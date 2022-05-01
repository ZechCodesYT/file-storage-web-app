import fastapi
import logging

from server.database import db
from server.database.models.users import User
from server.database.models import BaseModel
from server.auth import hash_password, check_password_matches


API_app = fastapi.FastAPI()
logger = logging.getLogger("Server")


class PartialUser(BaseModel):
    name: str
    password: str


@API_app.post("/register")
async def register_user(user: PartialUser, conn=fastapi.Depends(db)):
    await User.create(user.name, hash_password(user.password), conn)
    user = await User.get_by("name", user.name, conn)
    await conn.commit()
    return {"message": "SUCCESS", "user-id": user[0].id}


@API_app.post("/login")
async def login_user(user_info: PartialUser, conn=fastapi.Depends(db)):
    user = await User.get_by("name", user_info.name, conn)
    if not user or not check_password_matches(user_info.password, user[0].password):
        return {"status": "FAILED", "message": f"User's name or password was incorrect. {user!r}"}

    return {"status": "SUCCESS", "user-id": user[0].id}
