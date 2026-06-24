from datetime import datetime
from enum import StrEnum
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
    created_at: datetime = Field(default_factory=datetime.utcnow)
