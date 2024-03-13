from typing import Union

from pydantic import BaseModel


class Result(BaseModel):
    msg: Union[str, None]
    data: Union[object, None]

    @staticmethod
    def success(data=None):
        return Result(msg="操作成功", data=data)

    @staticmethod
    def error(msg=None):
        return Result(msg=msg, data=None)
