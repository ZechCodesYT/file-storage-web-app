# File Storage Web App/Service
This is a simple file storage web app that I will build live on 
[YouTube](https://youtu.be/Mv06Ev4kDHs).

It will allow you to upload files to a web server and retrieve them later. It’ll have a web interface along with a CLI tool 
to upload.

## Technologies
This project will be built using Python 3.10 and will use SQLite for storage. I’ll be using 
[FastAPI](https://fastapi.tiangolo.com/) for the web app, [HTTPX](https://www.python-httpx.org/) for web requests, and 
[Typer](https://typer.tiangolo.com/) for the CLI. For styling the web app I’ll use [Bootstrap](https://getbootstrap.com/).

## Running
You will need to have Poetry installed. It will handle installing all of the package dependencies for the project. Once you have Poetry use the following commands to run the File Storage Service.
```shell
poetry install
poetry run python -m server
```

## To Do List
- [x] REST API using FastAPI
- [ ] CLI to upload/download files using Typer & HTTPX
- [ ] Build a simple web app using FastAPI
- [ ] Create a custom TCP protocol for syncing folders
- [ ] Create a background service that keeps a folder synced

## Videos
Here are the links for the recordings of each YouTube live coding session I've done for this project.

- [Part 0](https://youtu.be/Mv06Ev4kDHs?t=383)
