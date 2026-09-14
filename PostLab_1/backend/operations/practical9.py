import os
import cv2
import numpy as np

# Directory containing locally bundled official cascades
CASCADES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cascades"))

def get_cascade_path(cascade_filename):
    """Resolve cascade file path from local cascades dir or cv2 data."""
    local_path = os.path.join(CASCADES_DIR, cascade_filename)
    if os.path.exists(local_path):
        return local_path
    
    # Fallback to cv2.data if present
    cv_data_path = getattr(cv2.data, "haarcascades", None)
    if cv_data_path:
        fallback = os.path.join(cv_data_path, cascade_filename)
        if os.path.exists(fallback):
            return fallback
            
    raise FileNotFoundError(f"Haar cascade XML not found: {cascade_filename} (searched {local_path})")

def process_practical9(img, operation="detect_object", params=None):
    """
    Practical 9: Object Detection
    Uses OpenCV Haar Feature-based Cascade Classifiers.
    Target objects: Frontal Faces, Eyes, Smiles, Full Body Pedestrians.
    Draws professional bounding boxes and overlays detection statistics.
    """
    if params is None:
        params = {}

    target = params.get("target", "face")  # "face", "eye", "smile", "fullbody"
    scale_factor = float(params.get("scale_factor", 1.1))
    scale_factor = max(1.05, min(scale_factor, 1.5))
    min_neighbors = int(params.get("min_neighbors", 5))
    min_neighbors = max(1, min(min_neighbors, 15))

    cascade_files = {
        "face": ("haarcascade_frontalface_default.xml", "Frontal Face", (56, 189, 248)),     # Cyan
        "eye": ("haarcascade_eye.xml", "Eye", (168, 85, 247)),                               # Purple
        "smile": ("haarcascade_smile.xml", "Smile", (251, 191, 36)),                         # Amber
        "fullbody": ("haarcascade_fullbody.xml", "Pedestrian / Body", (34, 197, 94))          # Green
    }

    cascade_info = cascade_files.get(target, cascade_files["face"])
    cascade_filename, target_label, box_color = cascade_info

    cascade_path = get_cascade_path(cascade_filename)
    classifier = cv2.CascadeClassifier(cascade_path)
    if classifier.empty():
        raise RuntimeError(f"Failed to load Haar Cascade Classifier: {cascade_filename}")

    # Convert to grayscale for Haar feature computation
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img.copy()

    detections = classifier.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=(30, 30)
    )

    res = img.copy()
    if len(res.shape) == 2:
        res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)

    detected_count = len(detections)
    detected_boxes = []

    # Draw stylish bounding boxes
    for idx, (x, y, w, h) in enumerate(detections, 1):
        detected_boxes.append({"id": idx, "x": int(x), "y": int(y), "width": int(w), "height": int(h)})
        
        # Bounding box
        cv2.rectangle(res, (x, y), (x + w, y + h), box_color, 2)
        
        # Label tag background
        label_text = f"{target_label} #{idx}"
        (text_w, text_h), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        tag_y = max(y, text_h + 8)
        cv2.rectangle(res, (x, tag_y - text_h - 6), (x + text_w + 8, tag_y + 2), box_color, -1)
        cv2.putText(res, label_text, (x + 4, tag_y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 15, 25), 1, cv2.LINE_AA)

    # Top banner summary
    summary_text = f"Detected: {detected_count} {target_label}(s)"
    cv2.rectangle(res, (10, 10), (10 + len(summary_text) * 11, 42), (15, 23, 42), -1)
    cv2.rectangle(res, (10, 10), (10 + len(summary_text) * 11, 42), box_color, 1)
    cv2.putText(res, summary_text, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    info = {
        "practical": 9,
        "operation": "detect_object",
        "target": target,
        "target_label": target_label,
        "detected_count": detected_count,
        "detections": detected_boxes,
        "details": f"Executed OpenCV Haar Feature Cascade Detection ({cascade_filename}) with scaleFactor={scale_factor}, minNeighbors={min_neighbors}. Detected {detected_count} instance(s)."
    }
    filename = f"practical9_detect_{target}_{detected_count}found.png"

    return res, info, filename
