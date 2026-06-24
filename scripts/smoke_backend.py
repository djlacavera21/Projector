from io import BytesIO
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_video_feed() -> None:
    response = client.get("/api/videos")
    assert response.status_code == 200
    assert response.json()[0]["id"] == "projector-manifesto"


def test_video_search_and_detail() -> None:
    response = client.get("/api/videos", params={"q": "pipeline"})
    assert response.status_code == 200
    assert response.json()[0]["id"] == "temple-upload-pipeline"

    detail = client.get("/api/videos/temple-upload-pipeline")
    assert detail.status_code == 200
    assert detail.json()["status"] == "processing"


def test_instance_policy_and_stats() -> None:
    policy = client.get("/api/instance/policy")
    assert policy.status_code == 200
    assert policy.json()["trackers_allowed"] is False
    assert len(policy.json()["principles"]) >= 1

    stats = client.get("/api/instance/stats")
    assert stats.status_code == 200
    assert stats.json()["total_videos"] >= 2
    assert stats.json()["channels"] >= 1


def test_upload_validation_and_queue() -> None:
    bad = client.post(
        "/api/videos/upload",
        data={"title": "Bad upload"},
        files={"file": ("note.txt", BytesIO(b"not video"), "text/plain")},
    )
    assert bad.status_code == 400

    good = client.post(
        "/api/videos/upload",
        data={"title": "Field Report", "channel": "Projector Creator"},
        files={"file": ("clip.mp4", BytesIO(b"fake video bytes"), "video/mp4")},
    )
    assert good.status_code == 202
    assert good.json()["status"] == "queued"


if __name__ == "__main__":
    test_healthz()
    test_video_feed()
    test_video_search_and_detail()
    test_instance_policy_and_stats()
    test_upload_validation_and_queue()
    print("backend smoke checks passed")
