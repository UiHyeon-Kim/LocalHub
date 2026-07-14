from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.api.routers.import_data import router as import_router
from app.db.base import Base
from app.db.session import engine
from app.models.post import Post

app = FastAPI(title="LocalHub API")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(import_router)