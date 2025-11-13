from pydantic import BaseModel
from typing import Optional, List

# User
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True



# Token
class Token(BaseModel):
    access_token: str
    token_type: str

# Tasks
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    completed: bool
    owner_id: int
    class Config:
        orm_mode = True
