"""Routes Definitions"""
from fastapi import APIRouter
from app.api.v1.router import router as router_v1

router = APIRouter()

# Includes region routes

# v1
router.include_router(router_v1)
