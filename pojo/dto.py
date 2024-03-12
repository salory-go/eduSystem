
from typing import List, Union

from pydantic import BaseModel

class UserDTO(BaseModel):
    username: str
    password: str
    role: int

# class teacherDTO(BaseModel):
#     username: str
#     password: str
#     role: int
