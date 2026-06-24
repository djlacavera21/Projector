from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.models.video import Video, VideoCreate, VideoStatus, new_video_id

router = APIRouter(prefix="/videos", tags=["videos"])

_demo_videos: list[Video] = [
    Video(
        id="projector-manifesto",
        title="Projector Manifesto",
        channel="Projector Core",
        description="A privacy-first video platform bootstrap entry, ready to become an HLS asset.",
        hls_url="https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
    ),
    Video(
        id="temple-upload-pipeline",
        title="Temple Upload Pipeline",
        channel="Projector Labs",
        status=VideoStatus.processing,
        description="A sample processing record that previews how uploads move toward FFmpeg-backed HLS.",
    ),
]


def _find_video(video_id: str) -> Video:
    for video in _demo_videos:
        if video.id == video_id:
            return video
    raise HTTPException(status_code=404, detail="Video not found")


@router.get("", response_model=list[Video])
async def list_videos(status_filter: VideoStatus | None = None, q: str | None = None) -> list[Video]:
    videos = _demo_videos
    if status_filter is not None:
        videos = [video for video in videos if video.status == status_filter]
    if q:
        needle = q.casefold()
        videos = [
            video
            for video in videos
            if needle in video.title.casefold()
            or needle in video.channel.casefold()
            or needle in video.description.casefold()
        ]
    return videos


@router.get("/{video_id}", response_model=Video)
async def get_video(video_id: str) -> Video:
    return _find_video(video_id)


@router.post("", response_model=Video, status_code=status.HTTP_201_CREATED)
async def create_video_metadata(payload: VideoCreate) -> Video:
    video = Video(
        id=new_video_id(),
        title=payload.title,
        channel=payload.channel,
        description=payload.description,
        status=VideoStatus.queued,
    )
    _demo_videos.insert(0, video)
    return video


@router.post("/upload", response_model=Video, status_code=status.HTTP_202_ACCEPTED)
async def upload_video(
    title: str = Form(..., min_length=1, max_length=120),
    channel: str = Form("Projector Creator", min_length=1, max_length=80),
    description: str = Form("", max_length=500),
    file: UploadFile = File(...),
) -> Video:
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Upload must be a video file")

    video = Video(
        id=new_video_id("queued"),
        title=title,
        channel=channel,
        status=VideoStatus.queued,
        description=description or f"Queued upload: {file.filename}",
    )
    _demo_videos.insert(0, video)
    return video
