import json

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi_cdn_host import monkey_patch_for_docs_ui
from tortoise.contrib.fastapi import register_tortoise

from config.dbConfig import TORTOISE_ORM
from server.admin.router import admin
from server.common.router import common
from server.student.router import student
from server.teacher.router import teacher
from pojo.result import Result

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

monkey_patch_for_docs_ui(app)


# @app.middleware("http")
# async def m1(request: Request, call_next):
#     if request.headers.get('token') is None:
#         result = json.dumps(Result.error("未登录").model_dump())
#         return Response(status_code=401, media_type="application/json", content=result)
#
#     response = await call_next(request)
#     return response


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
