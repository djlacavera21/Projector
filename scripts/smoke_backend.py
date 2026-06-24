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


if __name__ == "__main__":
    test_healthz()
    test_video_feed()
    print("backend smoke checks passed")
