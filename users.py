from enum import Enum
from typing import Optional, Union, List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr
from starlette import status

router = APIRouter()

users: List["UserOut"] = []


class Role(str, Enum):
    ADMIN: str = "admin"
    USER: str = "user"
    TEACHER: str = "teacher"
    SALES: str = "sales"


# ----------------- Schemas ------------------
class UserCreate(BaseModel):  # DRF serializers
    username: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Union[str, None] = None
    avatar_url: str = 'http://example.com/default.jpg'


class UserOut(BaseModel):  # DRF serializers
    id: int
    username: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: str = 'http://example.com/default.jpg'
    role: Optional[Role] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    role: Optional[Role] = None


# ------ helpers -----

def get_user_or_404(user_id):
    try:
        return users[user_id]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@router.get('/', response_model=List[UserOut])
async def get_users():
    return users


@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED,
             summary="Create User (role tanlash orqali)")
async def create_user(user: UserCreate,
                      user_role: Role = Query(
                          Role.USER,
                          description="Yangi user uchun role (role body da emas.)")) -> UserOut:
    new_id = len(users)
    created_user = UserOut(id=new_id, role=user_role, **user.model_dump(exclude={"password"}))
    users.append(created_user)
    return created_user


@router.get('/{user_id}')
async def user_detail(user_id: int) -> UserOut:
    _ = get_user_or_404(user_id)
    return users[user_id]


@router.put("/{user_id}")
async def update_user(user_id: int, user: UserOut) -> UserOut:
    try:
        _ = get_user_or_404(user_id)
        users[user_id] = user
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.delete('/{user_id}')
async def delete_user(user_id: int):
    try:
        _ = get_user_or_404(user_id)
        del users[user_id]
        return {"status": status.HTTP_204_NO_CONTENT, "message": "Not content"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
