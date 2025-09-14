from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str  # required bo'lishi uchun qiymat bermang.
    description: str | None = None  # ixtiyoriy
    price: float
    tax: float | None = None


# GET metod body ni ololmaydi. Doim POST, PUT, DELETE
@router.post('/items/', response_model=Item)
async def create_item(item: Item):
    return item
