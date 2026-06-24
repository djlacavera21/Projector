from fastapi import APIRouter

from app.api.videos import demo_video_stats
from app.models.instance import InstancePolicy, InstanceStats, ModerationPrinciple

router = APIRouter(prefix="/instance", tags=["instance"])


@router.get("/policy", response_model=InstancePolicy)
async def get_instance_policy() -> InstancePolicy:
    return InstancePolicy(
        principles=[
            ModerationPrinciple(
                title="Privacy by default",
                summary="No mandatory account for viewing, no third-party trackers, and self-hostable data ownership.",
            ),
            ModerationPrinciple(
                title="Transparent rules",
                summary="Instance-level policy is explicit, minimal, and appealable instead of hidden in opaque algorithms.",
            ),
            ModerationPrinciple(
                title="Creator sovereignty",
                summary="Uploads enter a direct creator pipeline designed for subscriptions, tips, and portable audiences.",
            ),
        ],
    )


@router.get("/stats", response_model=InstanceStats)
async def get_instance_stats() -> InstanceStats:
    return InstanceStats(**demo_video_stats())
