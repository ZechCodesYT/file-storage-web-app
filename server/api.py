import fastapi
import logging

from server.database import db
from server.database.models.users import User
from server.database.models import BaseModel
from server.auth import hash_password


API_app = fastapi.FastAPI()
logger = logging.getLogger("Server")


class PartialUser(BaseModel):
    name: str
    password: str


@API_app.post("/register")
async def register_user(user: PartialUser, conn=fastapi.Depends(db)):
    await User.create(user.name, hash_password(user.password), conn)
    user = await User.get_by("name", user.name, conn)
    return {"message": "SUCCESS", "user-id": user[0].id}
