from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl


class VideoStatus(StrEnum):
    queued = "queued"
    processing = "processing"
    ready = "ready"
    failed = "failed"


class Video(BaseModel):
    id: str
    title: str
    channel: str
    status: VideoStatus = VideoStatus.ready
    description: str = ""
    thumbnail_url: HttpUrl | None = None
    hls_url: HttpUrl | None = None
    original_filename: str | None = None
    upload_path: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VideoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    channel: str = Field(default="Projector Creator", min_length=1, max_length=80)
    description: str = Field(default="", max_length=500)


def new_video_id(prefix: str = "video") -> str:
    return f"{prefix}-{uuid4().hex[:12]}"
