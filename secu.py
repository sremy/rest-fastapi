from fastapi import FastAPI, Header, HTTPException, Depends
from typing import Union
import time

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/secured")
async def secured(token: str = Depends(oauth2_scheme)):
    return {
        "message": "Hello secured World!",
        "token": token
    }


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print("password: " + form_data.password)
    return {"access_token": form_data.username, "token_type": "bearer"}


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


@app.post("/page/{id}", status_code=status.HTTP_201_CREATED)
async def create_page(id: str):
    items = ["1", "2", "3"]
    if id in items:
        raise HTTPException(status_code=409, detail="Item already exists")
    return {"id": id}


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


@app.get("/request")
async def print_address(request: Request):
    ip = request.client.host
    print(ip)
    return ip


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')
