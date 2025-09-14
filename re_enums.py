from __future__ import annotations
from typing import List, Optional

from fastapi import APIRouter, UploadFile
from enum import Enum

from pydantic import BaseModel

enum_app = APIRouter()


class SystemMode(str, Enum):
    DarkMode: str = "dark_mode"
    LightMode: str = "light_mode"
    Auto: str = "auto"


@enum_app.get('/')
async def switch_mode(mode: SystemMode):
    if mode is SystemMode.DarkMode:
        # logic
        return {"mode": mode, "msg": "Sistema dark rejimga o'tdi."}
    elif mode.value == 'light_mode':
        # logic
        return {"mode": mode, "msg": "Sistema light rejimga o'tdi."}
    # logic
    return {"mode": mode, "msg": "Sistema auto rejimga o'tdi."}


@enum_app.get('/file/{file_path:path}')
async def get_file(file_path: str, file: List[UploadFile]):
    return {"path": file_path}


fake_more_datas = [{"name": "Object 1"}, {"name": "Object 2"}, {"name": "Object 3"}, {"name": "Object 3"},
                   {"name": "Object 4"}]


@enum_app.get('/more_datas/')
async def more_datas(skip: int = 0, limit: int = 10):
    return fake_more_datas[skip: skip + limit]


@enum_app.get('/read_item/{item_id}')
async def read_item(item_id: int, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@enum_app.get('/items/{item_id}/')
async def short_item(item_id: int, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        # logic
        item.update({"q": q})
    if not short:
        # logic
        item.update({"description": "Very short"})
    # logic
    return item


class Product(BaseModel):
    product: str
    price: float
    amount: int
    unit: str | None = None
    is_active: bool = True


@enum_app.post('/model_products')
async def get_model_products(product: Product):
    return product
