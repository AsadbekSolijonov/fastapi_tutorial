from __future__ import annotations

import re
from pathlib import Path
from typing import Optional
from uuid import uuid4

import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException
from enum import Enum

from starlette import status

router = APIRouter()


class ModelName(str, Enum):
    alexnet = "alexnet"
    restnet = "restnet"
    lenet = "lenet"


@router.get('/{model_name}')
async def get_model(model_name: ModelName):
    print(model_name, model_name.value)
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep learning FTW"}

    if model_name.value == 'letnet':
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@router.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Bazz"}, {"item_name": "Quix"}]


# query parametrs
@router.get('/items/')
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# optinal parametr
@router.get('/items/{item_id}')
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@router.get('/users/{user_id}/items/{item_id}')
async def read_user_item(
        user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has long description"}
        )
    return item
