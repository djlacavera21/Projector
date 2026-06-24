from pathlib import Path
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.models.video import Video, VideoCreate, VideoStatus, new_video_id
from app.services.videos import create_video, get_video as fetch_video, list_videos as fetch_videos, video_stats

router = APIRouter(prefix="/videos", tags=["videos"])
UPLOAD_ROOT = Path("media/uploads")


def demo_video_stats() -> dict[str, int]:
    return video_stats()


def _find_video(video_id: str) -> Video:
    video = fetch_video(video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.get("", response_model=list[Video])
async def list_videos(status_filter: VideoStatus | None = None, q: str | None = None) -> list[Video]:
    return fetch_videos(status_filter=status_filter, q=q)


@router.get("/{video_id}", response_model=Video)
async def get_video(video_id: str) -> Video:
    return _find_video(video_id)


@router.post("", response_model=Video, status_code=status.HTTP_201_CREATED)
async def create_video_metadata(payload: VideoCreate) -> Video:
    return create_video(
        Video(
            id=new_video_id(),
            title=payload.title,
            channel=payload.channel,
            description=payload.description,
            status=VideoStatus.queued,
        )
    )


@router.post("/upload", response_model=Video, status_code=status.HTTP_202_ACCEPTED)
async def upload_video(
    title: str = Form(..., min_length=1, max_length=120),
    channel: str = Form("Projector Creator", min_length=1, max_length=80),
    description: str = Form("", max_length=500),
    file: UploadFile = File(...),
) -> Video:
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Upload must be a video file")

    video_id = new_video_id("queued")
    video_dir = UPLOAD_ROOT / video_id
    video_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename or "upload.bin").name
    upload_path = video_dir / safe_name

    with upload_path.open("wb") as destination:
        shutil.copyfileobj(file.file, destination)

    video = Video(
        id=video_id,
        title=title,
        channel=channel,
        status=VideoStatus.queued,
        description=description or f"Queued upload: {safe_name}",
        original_filename=safe_name,
        upload_path=str(upload_path),
    )
    return create_video(video)
