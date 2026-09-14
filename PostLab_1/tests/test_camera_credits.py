import os

def test_camera_and_developer_credits():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    with open("frontend/style.css", "r", encoding="utf-8") as f:
        css = f.read()

    with open("frontend/script.js", "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Camera Elements & Features
    assert "Use Camera" in html
    assert 'id="camera-modal"' in html
    assert 'id="camera-video-stream"' in html
    assert 'id="btn-capture-photo"' in html
    assert 'id="btn-retake-camera"' in html
    assert 'Capture Photo' in html

    # 2. Developer Credit in Footer and About Modal
    assert "Developed by Muneebur Rahman" in html
    assert ("S. B. Jain Institute of Technology, Management &amp; Research" in html or 
            "S. B. Jain Institute of Technology, Management & Research" in html)
    assert "Interactive Image Processing Lab using Python, OpenCV and Flask" in html

    # 3. JavaScript MediaDevices Implementation
    assert "async function openCameraModal" in js
    assert "function capturePhotoFromStream" in js
    assert "function stopCameraStream" in js
    assert "async function switchCamera" in js
    assert "navigator.mediaDevices.getUserMedia" in js
    assert "state.isFromCamera" in js

    # 4. CSS Classes & Profile Photo
    assert ".camera-btn" in css
    assert ".camera-stream-container" in css
    assert ".developer-credit-box" in css
    assert ".retake-btn" in css
    assert ".footer-credit" in css
    assert ".dev-profile-img" in css
    assert "muneebur-rahman.jpeg" in html

def test_profile_photo_route():
    from app import app
    client = app.test_client()
    res = client.get("/assets/muneebur-rahman.jpeg")
    assert res.status_code == 200
    assert len(res.data) > 100000

def test_camera_captured_image_processing():
    """Simulate a camera captured image being processed by the Flask backend across practicals."""
    import io
    import json
    from PIL import Image
    from app import app

    client = app.test_client()
    # Create simulated camera photo
    img = Image.new("RGB", (640, 480), color=(120, 180, 240))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Process camera photo with Practical 1 (RGB to Gray)
    data = {
        "image": (buf, "camera_photo_120849.png"),
        "practical": 1,
        "operation": "rgb_to_gray",
        "params": json.dumps({})
    }
    res = client.post("/api/process", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data["success"] is True
    assert "data:image/png;base64," in res_data["processed_image"]
