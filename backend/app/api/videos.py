from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.models.video import Video, VideoStatus

router = APIRouter(prefix="/videos", tags=["videos"])

_demo_videos: list[Video] = [
    Video(
        id="projector-manifesto",
        title="Projector Manifesto",
        channel="Projector Core",
        description="A privacy-first video platform bootstrap entry, ready to become an HLS asset.",
        hls_url="https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
    )
]


@router.get("", response_model=list[Video])
async def list_videos() -> list[Video]:
    return _demo_videos


@router.post("/upload", response_model=Video, status_code=status.HTTP_202_ACCEPTED)
async def upload_video(
    title: str = Form(..., min_length=1, max_length=120),
    channel: str = Form("Projector Creator", max_length=80),
    file: UploadFile = File(...),
) -> Video:
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Upload must be a video file")

    video = Video(
        id=f"queued-{len(_demo_videos) + 1}",
        title=title,
        channel=channel,
        status=VideoStatus.queued,
        description=f"Queued upload: {file.filename}",
    )
    _demo_videos.insert(0, video)
    return video
