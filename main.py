from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from typing import List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
posts_storage = []


@app.get("/ping")
async def ping():
    return PlainTextResponse("pong", status_code=200)


@app.get("/home", response_class=HTMLResponse)
async def home():
    html_content = "<html><body><h1>Welcome home!</h1></body></html>"
    return HTMLResponse(content=html_content, status_code=200)


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    html_404 = "<html><body><h1>404 NOT FOUND</h1></body></html>"
    return HTMLResponse(content=html_404, status_code=404)


class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime


@app.post("/posts", status_code=201)
async def create_posts(posts: List[Post]):
    posts_storage.extend(post.model_dump() for post in posts)
    return JSONResponse(content=posts_storage)

@app.get("/posts")
async def get_posts():
    return JSONResponse(content=posts_storage, status_code=200)

@app.put("/posts")
async def upsert_post(post: Post):
    found = False
    for i, existing in enumerate(posts_storage):
        if existing["title"] == post.title:
            posts_storage[i] = post.model_dump()
            found = True
            break
    if not found:
        posts_storage.append(post.model_dump())
    return JSONResponse(content=posts_storage)



