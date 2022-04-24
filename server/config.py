import json
import pathlib


def get_config():
    path = pathlib.Path.cwd() / "config.json"

    if not path.exists():
        return {"db-connection": "data.db"}

    with path.open() as file:
        return json.load(file)
