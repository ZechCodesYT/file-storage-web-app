# File Storage Web App/Service
This is a simple file storage web app that I will build live on 
[YouTube](https://youtu.be/Mv06Ev4kDHs).

It will allow you to upload files to a web server and retrieve them later. It’ll have a web interface along with a CLI tool 
to upload.

## Technologies
This project will be built using Python 3.10 and will use SQLite for storage. I’ll be using 
[FastAPI](https://fastapi.tiangolo.com/) for the web app, [HTTPX](https://www.python-httpx.org/) for web requests, and 
[Typer](https://typer.tiangolo.com/) for the CLI. For styling the web app I’ll use [Bootstrap](https://getbootstrap.com/).

## To Do List
- [ ] REST API using FastAPI
- [ ] CLI to upload/download files using Typer & HTTPX
- [ ] Build a simple web app using FastAPI
- [ ] Create a custom TCP protocol for syncing folders
- [ ] Create a background service that keeps a folder synced
