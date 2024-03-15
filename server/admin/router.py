

from fastapi import APIRouter
from server.admin.course import admin_course
from server.admin.user import admin_user

admin = APIRouter()
admin.include_router(admin_course)
admin.include_router(admin_user)