import uvicorn
from fastapi import FastAPI,Request,Response
from tortoise.contrib.fastapi import register_tortoise

from config.dbConfig import TORTOISE_ORM
from server.admin.course import course

from server.admin.user import user
from server.common.router import common
from util.result import Result
import json

app = FastAPI()

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=True,
)

# app.include_router(common,tags=["普通接口"])
app.include_router(student, tags=["学生接口"])
app.include_router(admin,tags=["管理员接口"])
app.include_router(teacher, tags=["管理员接口"])

# @app.middleware("http")
# async def m1(request: Request,call_next):
#     response = await call_next(request)
    # body = json.dumps(Result.error("未登录").__dict__).encode("utf-8")
    # response = Response(status_code=401, media_type="application/json",content=body)
    # return response


if __name__ == "__main__":
    uvicorn.run("main:app", port=8081, reload=True)