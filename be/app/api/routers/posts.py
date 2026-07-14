from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.post import Post

router = APIRouter(prefix="/api/posts", tags=["posts"])


class PostCreate(BaseModel):
    title: str
    content: str
    password: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    password: str


class PostDelete(BaseModel):
    password: str


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    password: str
    view_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=List[PostOut])
def list_posts(db: Session = Depends(get_db)):
    posts = (
        db.query(Post)
        .order_by(Post.created_at.desc(), Post.id.desc())
        .all()
    )
    return posts


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    post.view_count += 1
    db.commit()
    db.refresh(post)
    return post


@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    title = payload.title.strip()
    content = payload.content.strip()
    password = payload.password.strip()

    if not title or not content or not password:
        raise HTTPException(
            status_code=400,
            detail="title, content, and password are required",
        )

    post = Post(title=title, content=content, password=password)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if payload.password != post.password:
        raise HTTPException(status_code=403, detail="password mismatch")

    if payload.title is not None:
        post.title = payload.title.strip() or post.title

    if payload.content is not None:
        post.content = payload.content.strip() or post.content

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, payload: PostDelete, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if payload.password != post.password:
        raise HTTPException(status_code=403, detail="password mismatch")

    db.delete(post)
    db.commit()
    return None