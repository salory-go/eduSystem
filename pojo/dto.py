
from typing import List, Union

from pydantic import BaseModel

class loginDTO(BaseModel):
    userNumber: str
    password: str
    role: int

class addUserDTO(BaseModel):
    userNumber: str
    password: str
    name: str
    email: str
    role: int

# class teacherDTO(BaseModel):
#     username: str
#     password: str
#     role: int
