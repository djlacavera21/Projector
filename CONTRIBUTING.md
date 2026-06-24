# Contributing to Projector

Projector is in bootstrap mode. Contributions should move the platform toward a self-hostable MVP while preserving privacy, creator sovereignty, and transparent governance.

## Development Principles

- Prefer self-hosted, open-source components.
- Keep defaults privacy-respecting: no third-party trackers, no surprise telemetry, no mandatory social login.
- Make moderation and policy decisions transparent, appealable, and instance-controlled.
- Favor Docker-first workflows that are easy for independent operators to run.

## Local Development

1. Copy environment defaults:
   ```bash
   cp .env.example .env
   ```
2. Start the stack:
   ```bash
   docker compose up --build
   ```
3. Open the web app at <http://localhost:3000> and the API docs at <http://localhost:8000/docs>.

## Pull Requests

- Keep PRs focused and explain the user-facing impact.
- Include tests or smoke checks when possible.
- Document new environment variables in `.env.example`.
- Do not introduce tracking, analytics, or proprietary hosted dependencies without an explicit discussion.
