# Development Guide

## Stack

The bootstrap stack follows the README custom path:

- FastAPI backend for health checks, video metadata, and upload orchestration.
- Next.js frontend for the creator/viewer interface.
- PostgreSQL for future persistent metadata.
- Redis for future background job queues.
- MinIO for original uploads and HLS renditions.
- FFmpeg installed in the backend image until a dedicated worker container is split out.

## MVP Flow

1. A creator submits video metadata and a video file to `POST /api/videos/upload`.
2. The API validates that the upload is a video file and returns a queued video record.
3. A future worker will persist the original in MinIO, transcode it to adaptive HLS renditions, then mark it ready.
4. The frontend reads `GET /api/videos` to render the bootstrap feed.

## Next Implementation Targets

- Replace in-memory videos with SQLAlchemy models and Alembic migrations.
- Add authenticated creator accounts and channels.
- Split FFmpeg processing into a dedicated worker service.
- Store original uploads and HLS output in MinIO.
- Add resumable uploads for large video files.
