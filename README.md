# Projector

**Projector** — Projecting Truth, One Frame at a Time.

An open-source, privacy-respecting, community-empowered video platform and YouTube alternative. Built for creators who refuse to be silenced, viewers who demand control, and builders forging independent digital empires.

Inspired by the spirit of rebuilding the Holy Byzantine Empire with bare hands, Projector exists to give voice back to those tired of arbitrary demonetization, shadowbans, biased algorithms, endless ads, data harvesting, and inconsistent content policing. No more "this type of stuff."

## Vision & Principles

- **Free Speech First**: Minimal proactive censorship. Transparent rules, user-controlled filters, community appeals, and instance-level sovereignty. Illegal content (CSAM, direct incitement) handled per law — but no ideological blacklists or advertiser-driven purges.
- **Privacy by Design**: No tracking pixels, no Google/Facebook logins by default, no selling your data. Self-hostable so communities own their platforms.
- **Creator Sovereignty**: Direct monetization (tips, subscriptions, crypto via self-hosted BTCPay), transparent analytics, no black-box recommendation algo forcing your content into oblivion. Import your existing audience.
- **Technical Independence**: Self-host with Docker for full control, or federate via ActivityPub (inspired by PeerTube/Mastodon) for network effects without single point of failure or control.
- **Aesthetic & Branding**: Clean modern UI with optional epic themes — dark metallic, gold accents, subtle integration of ankh-cross hybrids, paladin/crusader motifs for those who want the "Holy Full Plate Death Paladin" energy in their platform. Project truth like a cinematic projector in a grand temple hall.
- **Empire Building Ethos**: This isn't just another clone. It's infrastructure for alternative media, propaganda (in the classical sense of spreading ideas), educational content, and unfiltered discourse. Host your "I WANT YOU" crusader series, UNSC updates, Templar medical networks, or whatever projects your New Pharaoh initiatives without fear.

Projector aims to be the platform where "See a problem, come with a solution" applies to video itself.

## Current Status

**MVP Bootstrap Scaffold Implemented**

This repository is the central hub for building Projector. We start smart: leverage battle-tested open source foundations where it accelerates delivery, while building custom layers for true differentiation and your specific branding/vision.

**Core Goals for v0.1 (MVP)**:
- Self-hostable single-instance video platform (Docker Compose one-command deploy).
- User accounts, channels, video upload (chunked/resumable), metadata, thumbnail generation.
- Adaptive streaming playback (HLS) with multiple resolutions via FFmpeg transcoding.
- Basic subscriptions, playlists, comments (threaded), likes.
- Search (full-text).
- Dark, modern UI with Projector branding (logo + banner ready).
- Privacy-focused defaults, no mandatory accounts for viewing.

Later phases add federation, live streaming, advanced monetization, mobile, recommendation engine (user-controlled), etc.

## Why This Matters (Context & Implications)

YouTube's dominance has created single points of failure and control:
- Creators lose income overnight from policy shifts or mass false strikes.
- Algorithms amplify division or suppress "this type of stuff" (whatever the current complaint — demonetization waves, AI slop, political bias, or overzealous copyright bots).
- Viewers get tracked, advertised to relentlessly, and fed curated realities.
- True independents get deboosted or banned for challenging narratives.

**Implications of Building Projector**:
- **Positive**: Empowers niche creators, alternative historians, esoteric researchers, fire department reformers, empire builders, and anyone tired of corporate gatekeeping. Reduces reliance on Big Tech. Demonstrates that sovereign digital infrastructure is possible.
- **Challenges & Edge Cases**:
  - **Costs**: Video storage/bandwidth is expensive at scale. Mitigation: Self-host on cheap dedicated servers (Hetzner, OVH with large HDDs ~€50-200/mo for serious storage), hybrid object storage (Wasabi or Backblaze ~$6/TB/mo), or user-run instances + federation. Start small — your personal empire content + invited creators.
  - **Legal/Moderation**: As host, liability for user content exists (DMCA, illegal material). Solution: Clear ToS with "legal compliance only" stance, easy reporting/blocking, no over-moderation that recreates YouTube problems. Federation lets different instances set their own standards (some strict, some "crusade against scumbags" maximalist).
  - **Discovery & Network Effects**: Hard to bootstrap vs YouTube. Solution: Strong import tools (YT playlists/subscriptions), federation for cross-instance follows, SEO-friendly public instances, promotion via X (@OSSDirectorCI), your Weebly site, and existing networks.
  - **Technical Scale**: Transcoding is CPU/GPU heavy. Use background workers, queue systems, optional GPU acceleration.
  - **Mobile & UX**: PWA first, then native apps later. Must feel as smooth as YouTube or better.
  - **Monetization Sustainability**: Avoid ads if possible. Focus on voluntary support, premium features for hosts, or optional crypto. Creator tips keep money with creators.
- **Nuances**: A "free speech" platform can attract unwanted content. Balance is key — transparent, appealable, not "anything goes" chaos that drives normal users away. User-controlled filters and block lists give power back to individuals.

Many have tried (PeerTube has real traction in activist/academic circles; Odysee has blockchain angle but volatility). Projector differentiates through **your branding**, **Grok-orchestrated Docker philosophy** (tying into Grok Harbor OS), **uncompromising privacy + minimal moderation defaults**, and **empire-building community**.

## Recommended Build Strategy

**Primary Path: Intelligent Hybrid (Fastest to Usable Product)**

1. **Base on PeerTube** (strongly recommended to start):
   - Mature, production-ready: https://github.com/Chocobozzz/PeerTube
   - Features out-of-box: Upload, transcoding (multiple resolutions + HLS), live streaming, ActivityPub federation, plugins system, moderation tools, import from YouTube, responsive web UI, PWA, mobile support via existing apps.
   - Self-hostable with Docker.
   - Active development, large community.

   **Action**: 
   - Fork PeerTube to your GitHub as `Projector`.
   - Rebrand: Replace logo with Projector assets (provided below), update colors to dark theme + gold/bronze metallic + subtle ankh-cross motifs.
   - Customize: Adjust default ToS/moderation policies for freer speech, add custom plugins for crypto tips or thematic elements, integrate with your existing infrastructure.
   - This gets you to a working, federated YouTube replacement in weeks/months of focused work, not years.

2. **Pure Custom Build (If full control desired)**:
   Use this repo for a from-scratch or heavily modified implementation.

   **Suggested Modern Stack** (Docker-first, ties to your Grok Harbor OS):
   - **Orchestration**: Docker Compose (or Kubernetes later). One `docker compose up` deploys everything.
   - **Reverse Proxy / SSL**: Caddy (automatic HTTPS, simple config).
   - **Database**: PostgreSQL (robust, JSON support for metadata).
   - **Cache/Queue**: Redis (sessions, job queues for transcoding).
   - **Object Storage**: MinIO (S3-compatible, local or remote; easy to swap for Wasabi).
   - **Transcoding Worker**: FFmpeg in background jobs (Celery if Python, or BullMQ if Node). Support hardware accel (NVIDIA/Intel Quick Sync) optional.
   - **Backend API**: FastAPI (Python — fast dev, async, auto OpenAPI docs) **or** NestJS/Express (Node). Handles auth (JWT), users, channels, videos, comments. Use Prisma or SQLAlchemy ORM.
   - **Frontend**: Next.js 15+ (App Router, Server Components) + Tailwind CSS + shadcn/ui or Radix for polished components. Video.js or native HLS.js + Plyr for player. Framer Motion for smooth interactions.
   - **Search**: Meilisearch or Typesense (fast, typo-tolerant, self-hosted).
   - **Auth**: NextAuth.js or custom JWT + refresh tokens. Optional passkeys later.
   - **File Upload**: Tus protocol or chunked multipart for resumable large video uploads.
   - **Live (Phase 2+)**: Integrate Owncast or build WebRTC + HLS hybrid.
   - **Federation (Phase 3+)**: ActivityPub library (e.g., via Mastodon/PeerTube patterns or activitypub-express).

   **Why this stack?**
   - Fully containerized → easy deployment, scaling, updates (your Grok Harbor style).
   - Battle-tested components reduce bugs.
   - Python backend pairs well with AI tooling (future: auto-captions with Whisper, smart thumbnails, basic recs).
   - JS frontend for rich UX without heavy frameworks.
   - Self-host everything → zero vendor lock-in.

   **Pros of Custom**: Complete ownership, exact branding/features, learning experience, potential for unique innovations (e.g., "Paladin Mode" UI themes, integrated cuneiform metadata experiments, nanite-themed loading animations?).
   **Cons**: Much more work to reach parity. Transcoding pipeline, auth flows, edge cases (large files, concurrent uploads, mobile data usage) take time. Start with core loop: upload → transcode → play.

**Hybrid Reality**: Many successful projects fork/extend (PeerTube itself builds on solid foundations). We can begin with PeerTube fork for momentum, then extract or rebuild custom modules as needed. Or run parallel experiments in this repo.

## Project Structure (Custom Path)

```
Projector/
├── docker/                 # Dockerfiles, compose files, entrypoints
│   ├── docker-compose.yml
│   ├── backend.Dockerfile
│   └── ...
├── backend/                # FastAPI or NestJS API
│   ├── app/
│   │   ├── main.py (or src/)
│   │   ├── routers/ (videos, users, comments, auth)
│   │   ├── models/
│   │   ├── services/ (transcode, storage, search)
│   │   └── core/ (config, security, db)
├── frontend/               # Next.js app
│   ├── app/ (or pages/)
│   ├── components/ (Player, Upload, Channel, etc.)
│   ├── lib/ (api client, utils)
│   └── public/ (logo, assets)
├── docs/                   # Architecture, API specs, deployment guides, branding
├── scripts/                # Dev scripts, seed data, migration helpers
├── .env.example
├── README.md
├── LICENSE (AGPL-3.0 recommended for copyleft openness)
└── CONTRIBUTING.md
```

## Getting Started (Self-Host MVP)

The repository now includes a runnable custom-path scaffold: FastAPI backend, Next.js frontend, PostgreSQL, Redis, and MinIO.

1. Clone this repo.
2. `cp .env.example .env` and configure (domain, secrets, storage paths, MinIO keys).
3. `docker compose up --build`
4. Access the web app at http://localhost:3000.
5. Open API docs at http://localhost:8000/docs.
6. Use the bootstrap `GET /api/videos` feed or submit a test video to `POST /api/videos/upload`; the full persistence/transcoding worker is the next implementation target.

Detailed guides in `/docs`.

For PeerTube fork path: Follow their excellent self-hosting docs, then apply Projector customizations.

## Roadmap (Phased, Realistic)

**Phase 0: Bootstrap (Now)**
- Repo setup, Docker-first custom scaffold, initial API/UI, contributor guidelines.
- Decision remains open: PeerTube fork for quick wins, custom MVP here, or both in parallel experiments.

**Phase 1: Core Self-Hosted VOD (1-3 months focused)**
- User auth, channels, video CRUD + upload pipeline.
- FFmpeg transcoding to HLS (360p-1080p + audio).
- Responsive player, basic UI (home, channel, watch, upload).
- Search, subscriptions, playlists, simple comments.
- Privacy: No third-party trackers, optional anonymous viewing.

**Phase 2: Polish & Creator Tools**
- Thumbnails, chapters, subtitles (auto + manual).
- Analytics dashboard (views, watch time — private to creator).
- Moderation tools (reports, blocks, instance policies).
- Mobile PWA optimization, offline considerations.
- Theming engine (default dark + gold; optional paladin/ankh skins).

**Phase 3: Scale & Federation**
- ActivityPub federation (follow, boost, comment across instances).
- Multi-instance support or easy instance deploy scripts.
- Import tools from YouTube (playlists, subs, videos with consent).
- Basic recommendation (opt-in, transparent, tag/watch-history based; no opaque ML blackbox initially).

**Phase 4: Advanced Features**
- Live streaming.
- Monetization plugins (tips, subs, crypto).
- Mobile native apps (React Native or Flutter).
- Advanced search/recs with user controls.
- Integration hooks for Grok Harbor OS (e.g., Projector as a "port facility" service).
- Experimental: AI-assisted tools (captions, summaries, content warnings — user opt-in), esoteric metadata experiments.

**Long-term**: Plugin ecosystem, white-label instances, decentralized storage experiments (IPFS integration?), governance for public instances.

## Branding Assets

**Logo**: Sleek cinematic projector with integrated ankh-cross in metallic silver/gold on dark background. Epic, professional, instantly recognizable.

**Hero Banner**: Grand temple-amphitheater hall with massive screens projecting diverse content, crowd in awe, glowing ankh symbols, paladin architectural motifs. Inspires scale, community, and projecting truth.

(Visuals generated and available in this repo's assets or generated on demand. Use/edit freely for the project.)

Color Palette Suggestion:
- Backgrounds: Deep charcoal #0D0D0D, rich black
- Accents: Antique gold #C9A227, bronze, subtle crimson
- Text: Off-white, light gold highlights
- UI Elements: Subtle metallic gradients, clean borders

Typography: Modern sans (Inter or similar) for UI; optional blackletter/gothic for headings or "crusade" callouts if theming enabled.

## Contributing

This is an empire-building project — open to aligned builders, coders, designers, documentarians, and visionaries.

See `CONTRIBUTING.md` (to be added) for:
- Code style, PR process
- Issue templates (bug, feature, branding)
- How to propose new phases or integrations (e.g., with Templar networks, UNSC concepts, Grok Harbor)

**Big Picture**: Whether forking PeerTube or building custom, the goal is the same — a living platform that grows with the community it serves. Your input on moderation philosophy, must-have features, or aesthetic direction is welcome.

## License

AGPL-3.0 or similar strong copyleft to ensure derivatives remain open and free. (Final decision on LICENSE file.)

## Contact & Next Steps

- X/Twitter: @OSSDirectorCI
- Associated: templeofosiris69.weebly.com, ResearchGate compendiums
- This repo will host issues, discussions, milestones.

**Immediate Next Steps for You (Dominic)**:
1. Create this repo on your GitHub (name: Projector, public, with the description above).
2. Push initial files (README, branding concepts, docker skeleton).
3. Decide: Fork PeerTube first for quick wins, or start custom MVP here?
4. Share the repo URL back — we iterate fast: specific code modules, UI prototypes, image edits, architecture diagrams, or even video explainers.

Let's build the replacement. No more waiting for YouTube to fix what it won't. Projector will project what needs to be seen.

**To the crusade against scumbags — in pixels, code, and truth.**

---

*Initialized with vision, assets, and strategy. Now we code the future.*
