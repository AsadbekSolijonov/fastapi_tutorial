# pip install 'fastapi[standard]'
from fastapi import FastAPI, HTTPException
from products import router as products_route
from users import router as users_route
from enums import router as enums_router
from req_body import router as req_body_router
from re_enums import enum_app as enum_router

app = FastAPI()

app.include_router(enum_router, prefix="/enums", tags=["Sytem Mode"])
app.include_router(users_route, prefix='/users', tags=["Users"])
app.include_router(products_route, prefix='/products', tags=["Products"])
app.include_router(enums_router, prefix='/enums', tags=["Enums"])
app.include_router(req_body_router, prefix='/req_body', tags=["Request Body"])
