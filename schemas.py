from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from models import TaskStatus


# ── User Schemas ──────────────────────────────────────────────────

class UserCreate(BaseModel):
    email:    EmailStr
    username: str = Field(min_length=3, max_length=50, pattern=r"^\w+$")
    password: str = Field(min_length=8, max_length=100)


class UserResponse(BaseModel):
    id:         int
    email:      EmailStr
    username:   str
    is_active:  bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# ── Task Schemas ──────────────────────────────────────────────────

class TaskCreate(BaseModel):
    title:       str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_priority: bool = False


class TaskUpdate(BaseModel):
    title:       Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status:      Optional[TaskStatus] = None
    is_priority: Optional[bool] = None


class TaskResponse(BaseModel):
    id:          int
    title:       str
    description: Optional[str]
    status:      TaskStatus
    is_priority: bool
    owner_id:    int
    created_at:  datetime
    updated_at:  Optional[datetime]

    model_config = {"from_attributes": True}


class TaskWithOwner(TaskResponse):
    owner: UserResponse
