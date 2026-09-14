import io
import json
import pytest
from PIL import Image
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def create_test_image_bytes():
    """Generate in-memory PNG image bytes."""
    img = Image.new("RGB", (100, 100), color=(100, 150, 200))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "online"
    assert data["practicals_count"] == 11

def test_homepage_serves(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Image Processing Lab" in res.data

def test_api_process_p1_gray(client):
    buf = create_test_image_bytes()
    data = {
        "image": (buf, "test.png"),
        "practical": 1,
        "operation": "rgb_to_gray",
        "params": json.dumps({})
    }
    res = client.post("/api/process", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data["success"] is True
    assert "data:image/png;base64," in res_data["processed_image"]
    assert res_data["filename"] == "practical1_rgb_to_gray.png"

def test_api_compress_p7(client):
    buf = create_test_image_bytes()
    data = {
        "image": (buf, "test.png"),
        "quality": 40
    }
    res = client.post("/api/compress", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data["success"] is True
    assert res_data["info"]["quality"] == 40
    assert "data:image/jpeg;base64," in res_data["processed_image"]

def test_api_detect_p9(client):
    buf = create_test_image_bytes()
    data = {
        "image": (buf, "test.png"),
        "params": json.dumps({"target": "face", "min_neighbors": 1})
    }
    res = client.post("/api/detect", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data["success"] is True
    assert "detected_count" in res_data["info"]
