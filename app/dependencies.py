from typing import Annotated
from fastapi import Header, HTTPException
import os

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != os.getenv("API_SECRET_KEY"):
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != os.getenv("QUERY_SECRET_KEY"):
        raise HTTPException(status_code=400, detail="Invalid query token")
