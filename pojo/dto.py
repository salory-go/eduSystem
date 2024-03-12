from datetime import datetime
from typing import List, Union
from typing import Optional
from pydantic import BaseModel


class loginDTO(BaseModel):
    userNumber: str
    password: str
    role: int


class UserDTO(BaseModel):
    userNumber: Optional[str]
    password: Optional[str]
    name: Optional[str]
    email: Optional[str]
    role: Optional[int]

# class teacherDTO(BaseModel):
#     username: str
#     password: str
#     role: int
