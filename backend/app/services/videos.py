from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator
from urllib.parse import urlparse

from app.core.config import settings
from app.models.video import Video, VideoStatus

_SCHEMA = """
CREATE TABLE IF NOT EXISTS videos (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    channel TEXT NOT NULL,
    status TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    thumbnail_url TEXT,
    hls_url TEXT,
    original_filename TEXT,
    upload_path TEXT,
    created_at TEXT NOT NULL
);
"""

_BOOTSTRAP_VIDEOS = [
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


def _database_path() -> Path:
    parsed = urlparse(settings.database_url)
    if parsed.scheme not in {"sqlite", "sqlite+pysqlite", "sqlite+aiosqlite"}:
        return Path("projector.db")
    if parsed.path in {"", "/"}:
        return Path("projector.db")
    if parsed.netloc:
        return Path(f"/{parsed.netloc}{parsed.path}")
    return Path(parsed.path.lstrip("/"))


DB_PATH = _database_path()


@contextmanager
def _connect() -> Iterator[sqlite3.Connection]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_video_store() -> None:
    with _connect() as connection:
        connection.execute(_SCHEMA)
        count = connection.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
        if count == 0:
            for video in _BOOTSTRAP_VIDEOS:
                _insert(connection, video)


def _row_to_video(row: sqlite3.Row) -> Video:
    return Video(
        id=row["id"],
        title=row["title"],
        channel=row["channel"],
        status=VideoStatus(row["status"]),
        description=row["description"],
        thumbnail_url=row["thumbnail_url"],
        hls_url=row["hls_url"],
        original_filename=row["original_filename"],
        upload_path=row["upload_path"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _insert(connection: sqlite3.Connection, video: Video) -> None:
    connection.execute(
        """
        INSERT INTO videos (id, title, channel, status, description, thumbnail_url, hls_url, original_filename, upload_path, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            video.id,
            video.title,
            video.channel,
            video.status.value,
            video.description,
            str(video.thumbnail_url) if video.thumbnail_url else None,
            str(video.hls_url) if video.hls_url else None,
            video.original_filename,
            video.upload_path,
            video.created_at.isoformat(),
        ),
    )


def create_video(video: Video) -> Video:
    init_video_store()
    with _connect() as connection:
        _insert(connection, video)
    return video


def list_videos(status_filter: VideoStatus | None = None, q: str | None = None) -> list[Video]:
    init_video_store()
    query = "SELECT * FROM videos"
    clauses: list[str] = []
    params: list[str] = []
    if status_filter is not None:
        clauses.append("status = ?")
        params.append(status_filter.value)
    if q:
        clauses.append("(LOWER(title) LIKE ? OR LOWER(channel) LIKE ? OR LOWER(description) LIKE ?)")
        needle = f"%{q.casefold()}%"
        params.extend([needle, needle, needle])
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY datetime(created_at) DESC"
    with _connect() as connection:
        rows = connection.execute(query, params).fetchall()
    return [_row_to_video(row) for row in rows]


def get_video(video_id: str) -> Video | None:
    init_video_store()
    with _connect() as connection:
        row = connection.execute("SELECT * FROM videos WHERE id = ?", (video_id,)).fetchone()
    return _row_to_video(row) if row else None


def video_stats() -> dict[str, int]:
    videos = list_videos()
    channels = {video.channel for video in videos}
    return {
        "total_videos": len(videos),
        "ready_videos": sum(video.status == VideoStatus.ready for video in videos),
        "queued_videos": sum(video.status == VideoStatus.queued for video in videos),
        "processing_videos": sum(video.status == VideoStatus.processing for video in videos),
        "channels": len(channels),
    }
