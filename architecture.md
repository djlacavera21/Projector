# Projector Architecture

## Overview
Custom-built, self-hosted video platform emphasizing privacy, control, and your branding (dark metallic + gold + ankh-cross motifs). Docker-first for easy deployment and alignment with Grok Harbor OS.

**Core Philosophy**:
- Start small: MVP = upload → transcode (FFmpeg) → adaptive HLS playback.
- Self-host everything (no vendor lock-in).
- Minimal moderation defaults + transparent policies.
- Extensible for federation later (ActivityPub).
- Branding: Epic, truth-projecting aesthetic.

## High-Level Components

1. **Reverse Proxy & TLS**: Caddy (auto HTTPS, simple config).
2. **Object Storage**: MinIO (S3-compatible) for original videos + transcoded HLS segments.
3. **Database**: PostgreSQL (async with SQLAlchemy 2.0) for metadata (users, videos, channels, comments, likes, subscriptions).
4. **Cache & Queue**: Redis (sessions, Celery/RQ broker for transcoding jobs).
5. **Backend API**: FastAPI (async, auto OpenAPI docs at /docs). Handles auth (JWT), CRUD, upload orchestration.
6. **Transcoding Worker**: Separate container/process using FFmpeg. Downloads original from MinIO, generates multiple resolutions + HLS manifests, uploads back, updates DB status.
7. **Frontend**: Next.js 15+ (App Router). Modern UI with Tailwind, shadcn/ui. Dark theme + gold accents. Video player (HLS.js + Plyr or Video.js). Upload form with progress.
8. **Optional later**: Meilisearch for fast search, Celery for tasks, Whisper for auto-captions, etc.

## Data Flow (MVP Video Upload)
1. User uploads via frontend → POST /api/videos/upload (chunked/resumable recommended for large files).
2. Backend validates, generates video_id, uploads original to MinIO (originals/{id}/file.mp4).
3. Backend creates DB record (status: "processing"), queues transcoding job to Redis.
4. Worker picks job: Downloads original, runs FFmpeg pipeline (e.g., 1080p, 720p, 480p + audio → HLS segments + master.m3u8).
5. Worker uploads HLS files to MinIO (videos/{id}/hls/...), updates DB status to "ready".
6. User views: Frontend fetches metadata + HLS URL (presigned or proxied), plays with adaptive quality.

## Security & Privacy
- JWT auth with refresh tokens.
- File validation (MIME, size limits, virus scan placeholder).
- Presigned URLs with expiration for MinIO access.
- No unnecessary tracking.
- Clear ToS: Legal compliance only for moderation.

## Scaling & Production Notes
- Start single VPS (Hetzner/OVH with large storage).
- For scale: Multiple workers, CDN in front of MinIO (or Bunny.net), read replicas for DB.
- Costs: Storage primary concern — use cheap object storage or self MinIO on big disks.
- Monitoring: Add Prometheus + Grafana later.
- Backups: Regular DB + MinIO snapshots.

## Branding Integration
- UI: Dark backgrounds (#0D0D0D), gold accents (#C9A227), subtle ankh-cross in logo/favicon.
- Theming: Optional "Paladin Mode" or crusade-themed elements.
- Content focus: Easy hosting for your propaganda series, empire updates, etc.

## Roadmap Alignment
See main README for phased plan. This architecture supports Phase 1 MVP directly and scales to later features.

Next steps: Implement auth, DB models (Alembic), full transcoding pipeline, basic frontend player + upload UI.

Questions or iterations? This is designed for rapid MVP while keeping it production-viable.