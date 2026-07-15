from fastapi import FastAPI

from app.api.routers.chat import router as chat_router
from app.api.routers.health import router as health_router
from app.api.routers.import_data import router as import_router
from app.api.routers.posts import router as posts_router
from app.db.base import Base
from app.db.session import engine


app = FastAPI(
    title="LocalHub API",
    version="1.0.0",
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(import_router)
app.include_router(posts_router)
app.include_router(chat_router)
