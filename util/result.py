from typing import Union

from pydantic import BaseModel


class Result(BaseModel):
    msg: Union[None, str]
    code: int
    data: Union[object, None]

    @staticmethod
    def success(object=None):
        return Result(msg="success", data=object)

    @staticmethod
    def error(msg=None):
        return Result(msg=msg, data=None)
