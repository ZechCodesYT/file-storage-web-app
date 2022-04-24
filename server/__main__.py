import logging


logging.basicConfig(level=logging.DEBUG)   # add this line
logging.getLogger("aiosqlite").setLevel(logging.INFO)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", port=8000, log_level="debug")
