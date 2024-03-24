import json

import uvicorn
from fastapi import FastAPI, Request, Response
from tortoise.contrib.fastapi import register_tortoise

from const.dbConfig import TORTOISE_ORM
from const.path import path
from server.admin.router import admin
from server.common.router import common
from server.student.router import student
from server.teacher.router import teacher
from pojo.result import Result
from task.assignmentTask import scheduler
from util.jwtToken import verify

app = FastAPI()

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=True,
)

app.include_router(common, tags=["普通接口"])
app.include_router(admin, prefix='/admin', tags=["管理员接口"])
app.include_router(teacher, prefix='/teacher', tags=["教师接口"])
app.include_router(student, prefix='/student', tags=["学生接口"])


# @app.middleware("http")
# async def m1(request: Request, call_next):
#     token = request.headers.get('token')
#     print(request.url.path)
#     if (request.url.path not in path and
#             (token is None or verify(token) is False)):
#         result = json.dumps(Result.error("请登录！").model_dump())
#         return Response(status_code=401, media_type="application/json", content=result)
#
#     response = await call_next(request)
#     return response


@app.on_event("startup")
async def start_scheduler():
    scheduler.start()


@app.on_event("shutdown")
async def stop_scheduler():
    scheduler.shutdown()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, log_level="info")
