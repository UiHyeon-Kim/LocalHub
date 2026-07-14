from fastapi import FastAPI
from app.api.routers.health import router as health_router
from app.api.routers.import_data import router as import_router

app = FastAPI(title="LocalHub API")
app.include_router(health_router)
app.include_router(import_router)