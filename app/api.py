from fastapi import APIRouter
from app.modules.auth.endpoints import router as auth_router
from app.modules.departments.endpoints import router as departments_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(departments_router, prefix="/departments", tags=["Departments"])
