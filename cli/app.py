import typer
import cli.auth
import cli.sync
import pathlib


app = typer.Typer()


@app.command()
def main():
    typer.echo("Hello World")


@app.command()
def login(username: str, password: str):
    cli.auth.login(username, password)


@app.command()
def register(username: str, password: str):
    user_id = cli.auth.register(username, password)
    if user_id is None:
        typer.secho("Failed to register", fg=typer.colors.RED)


@app.command()
def sync(folder_name: str):
    cli.sync.sync_folder(folder_name, pathlib.Path().resolve())
