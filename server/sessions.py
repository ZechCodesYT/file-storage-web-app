from random import randbytes
from base64 import b64encode
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from server.database import db
from server.database.models.sessions import Session
from time import time
import json


oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token():
    data = bytearray(randbytes(24))
    data[:4] = int(time()).to_bytes(4, "big")
    return b64encode(data).decode()


async def get_session(token: str = Depends(oauth_scheme), conn=Depends(db)):
    session = await Session.get(token, conn)
    if not session or session.expires < time():
        return {}

    await session.refresh(conn)
    return json.loads(session.data)
