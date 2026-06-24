from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class Comment(BaseModel):
    id: str
    video_id: str
    author: str = Field(..., min_length=1, max_length=80)
    body: str = Field(..., min_length=1, max_length=500)
    parent_id: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CommentCreate(BaseModel):
    author: str = Field(default="Projector Viewer", min_length=1, max_length=80)
    body: str = Field(..., min_length=1, max_length=500)
    parent_id: str | None = None


def new_comment_id() -> str:
    return f"comment-{uuid4().hex[:12]}"
