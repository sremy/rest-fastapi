from fastapi import FastAPI, Header, HTTPException
from typing import Union
import time

from starlette import status
from starlette.requests import Request

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/page/{id}")
async def page_id(id: int):
    seconds = time.time()
    return {"Page": id,
            "timestamp": seconds,
            "localtime": time.localtime(seconds),
            "date": time.ctime()}


@app.get("/search/")
async def search_item(author: str, book: str):
    return f"Searching author={author} and book={book}"


# Simple addition
@app.get("/add")
def add(a: int = 0, b: int = 0):
    return a + b


@app.get("/{folder}/{file}")
def add(folder: str, file: str):
    return {
        "folder": folder,
        "file": file
    }


# Create a new page with a POST call
@app.post("/page/{id}", status_code=status.HTTP_201_CREATED)
async def create_page(id: str):
    items = ["1", "2", "3"]
    if id in items:
        raise HTTPException(status_code=409, detail="Item already exists")
    return {"id": id}


# Returns HTTP headers
@app.get("/headers")
async def print_header(user_agent: Union[str, None] = Header(default=None),
                       accept=Header(default=None),
                       accept_encoding=Header(default=None),
                       accept_language=Header(default=None),
                       host=Header(default=None),
                       authentication=Header(default=None)
                       ):
    print(accept)
    return {
        "user_agent": user_agent,
        "accept": accept,
        "accept_encoding": accept_encoding,
        "accept_language": accept_language,
        "host": host,
        "authentication": authentication
    }


# Returns the client IP address
@app.get("/request")
async def print_address(request: Request):
    ip = request.client.host
    print(ip)
    return ip


def print_usage():
    print('uvicorn main:app --reload')


if __name__ == '__main__':
    print_usage()
