from fastapi import APIRouter

interceptor = APIRouter()

# @interceptor.middleware("http")
# async def m1(request: Request,call_next):
#     response = await call_next(request)
#     response.body = Result.error("未登录")
#     print("1")
#
#     return response