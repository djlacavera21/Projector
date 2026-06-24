from pydantic import BaseModel, Field


class ModerationPrinciple(BaseModel):
    title: str
    summary: str


class InstancePolicy(BaseModel):
    name: str = "Projector Sovereign Instance"
    tagline: str = "Projecting truth, one frame at a time."
    viewing_requires_account: bool = False
    trackers_allowed: bool = False
    monetization_default: str = "creator-direct"
    federation_phase: str = "planned"
    principles: list[ModerationPrinciple] = Field(default_factory=list)


class InstanceStats(BaseModel):
    total_videos: int
    ready_videos: int
    queued_videos: int
    processing_videos: int
    channels: int
