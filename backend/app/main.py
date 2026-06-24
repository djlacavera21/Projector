from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.api.instance import router as instance_router
from app.api.videos import router as videos_router
from app.services.videos import init_video_store

app = FastAPI(
    title="Projector API",
    version="0.1.0",
    description="Privacy-respecting, self-hostable video platform API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    init_video_store()


app.include_router(health_router)
app.include_router(instance_router, prefix="/api")
app.include_router(videos_router, prefix="/api")


@app.get("/")
async def root() -> dict[str, str]:
    return {"name": "Projector", "message": "Projecting truth, one frame at a time."}
