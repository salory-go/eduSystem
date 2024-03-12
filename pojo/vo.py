from datetime import date
from typing import List, Union

from pydantic import BaseModel

class UserVO(BaseModel):
    id: str
    token: str