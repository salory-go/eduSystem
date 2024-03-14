from fastapi import APIRouter

from server.common.login import login

common = APIRouter()

common.include_router(login)

