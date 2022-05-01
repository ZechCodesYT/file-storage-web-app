import fastapi
import logging

from server.api import API_app
from server.database import db, run_migrations


app = fastapi.FastAPI()
logger = logging.getLogger("Server")


@app.on_event("startup")
async def startup_event():
    async for session in db():
        logger.info(f"starting database {session}")
        await run_migrations(session)


app.mount("/api/v1/", API_app)
