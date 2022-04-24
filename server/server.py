import fastapi
import logging

from server.database import db, run_migrations


app = fastapi.FastAPI()
logger = logging.getLogger("Server")


@app.on_event("startup")
async def startup_event():
    async for session in db():
        logger.info(f"starting database {session}")
        await run_migrations(session)


@app.get("/")
async def hello(db=fastapi.Depends(db)):
    return {"message": f"{db}"}
