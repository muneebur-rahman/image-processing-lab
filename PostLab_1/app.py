import json
import os
import time
import cv2
import numpy as np
from flask import Flask, jsonify, request, send_from_directory

from backend.utils import (
    decode_image_file,
    decode_mask_from_base64,
    encode_image_to_base64,
    is_allowed_file
)
from backend.operations.practical1 import process_practical1
from backend.operations.practical2 import process_practical2
from backend.operations.practical3 import process_practical3
from backend.operations.practical4 import process_practical4
from backend.operations.practical5 import process_practical5
from backend.operations.practical6 import process_practical6
from backend.operations.practical7 import process_practical7
from backend.operations.practical8 import process_practical8
from backend.operations.practical9 import process_practical9
from backend.operations.practical10 import process_practical10
from backend.operations.practical11 import process_practical11

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=FRONTEND_DIR)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload

# --- Static Routes ---
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

@app.route("/<path:filename>")
def serve_frontend_assets(filename):
    # Check frontend dir first
    if os.path.exists(os.path.join(FRONTEND_DIR, filename)):
        return send_from_directory(FRONTEND_DIR, filename)
    # Check static dir
    if os.path.exists(os.path.join(STATIC_DIR, filename)):
        return send_from_directory(STATIC_DIR, filename)
    return jsonify({"error": "Resource not found"}), 404

# --- Health / Info Endpoint ---
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "online",
        "opencv_version": cv2.__version__,
        "practicals_count": 11,
        "environment": "College Image Processing Laboratory"
    })

# --- Main Unified Processing Endpoint (Practicals 1-5, 8, 10, 11) ---
@app.route("/api/process", methods=["POST"])
def process_image():
    start_time = time.perf_counter()
    try:
        # Validate primary image
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image file uploaded."}), 400
        
        file_obj = request.files["image"]
        img, original_name, byte_len = decode_image_file(file_obj)
        h, w = img.shape[:2]

        practical_num = int(request.form.get("practical", 1))
        operation = request.form.get("operation", "").strip()

        # Parse parameters JSON
        params_raw = request.form.get("params", "{}")
        try:
            params = json.loads(params_raw) if params_raw else {}
        except Exception:
            params = {}

        # Handle secondary image if uploaded
        second_img = None
        if "second_image" in request.files:
            sec_file = request.files["second_image"]
            if sec_file.filename != "":
                second_img, _, _ = decode_image_file(sec_file)

        # Dispatch based on practical number
        if practical_num == 1:
            res_img, info, filename = process_practical1(img, operation, params, second_img)
        elif practical_num == 2:
            res_img, info, filename = process_practical2(img, operation, params)
        elif practical_num == 3:
            res_img, info, filename = process_practical3(img, operation, params)
        elif practical_num == 4:
            res_img, info, filename = process_practical4(img, operation, params)
        elif practical_num == 5:
            res_img, info, filename = process_practical5(img, operation, params)
        elif practical_num == 6:
            # If called via /api/process, inpaint mask must be provided
            mask_b64 = request.form.get("mask_b64")
            mask = decode_mask_from_base64(mask_b64, img.shape) if mask_b64 else None
            res_img, info, filename = process_practical6(img, operation, mask, params)
        elif practical_num == 7:
            res_img, comp_data_url, info, filename = process_practical7(img, byte_len, params)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return jsonify({
                "success": True,
                "practical": 7,
                "operation": "compress",
                "processed_image": comp_data_url,
                "filename": filename,
                "dimensions": {"width": w, "height": h},
                "execution_time_ms": elapsed_ms,
                "info": info
            })
        elif practical_num == 8:
            res_img, info, filename = process_practical8(img, operation, params)
        elif practical_num == 9:
            res_img, info, filename = process_practical9(img, operation, params)
        elif practical_num == 10:
            res_img, info, filename = process_practical10(img, operation, params)
        elif practical_num == 11:
            res_img, info, filename = process_practical11(img, operation, params)
        else:
            return jsonify({"success": False, "error": f"Invalid practical number: {practical_num}"}), 400

        # Encode processed image to base64
        processed_data_url, _ = encode_image_to_base64(res_img)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return jsonify({
            "success": True,
            "practical": practical_num,
            "operation": operation,
            "processed_image": processed_data_url,
            "filename": filename,
            "dimensions": {"width": w, "height": h},
            "execution_time_ms": elapsed_ms,
            "info": info
        })

    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Internal Processing Error: {str(e)}"}), 500

# --- Dedicated Inpainting Endpoint (Practical 6) ---
@app.route("/api/inpaint", methods=["POST"])
def inpaint_image():
    start_time = time.perf_counter()
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image uploaded."}), 400

        file_obj = request.files["image"]
        img, _, _ = decode_image_file(file_obj)
        h, w = img.shape[:2]

        operation = request.form.get("operation", "telea")
        params_raw = request.form.get("params", "{}")
        try:
            params = json.loads(params_raw) if params_raw else {}
        except Exception:
            params = {}

        # Mask retrieval
        mask_b64 = request.form.get("mask_b64")
        if not mask_b64 and "mask" in request.files:
            mask_file = request.files["mask"]
            if mask_file.filename != "":
                mask_raw = mask_file.read()
                nparr = np.frombuffer(mask_raw, np.uint8)
                mask = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
            else:
                mask = None
        elif mask_b64:
            mask = decode_mask_from_base64(mask_b64, img.shape)
        else:
            mask = None

        res_img, info, filename = process_practical6(img, operation, mask, params)
        processed_data_url, _ = encode_image_to_base64(res_img)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return jsonify({
            "success": True,
            "practical": 6,
            "operation": operation,
            "processed_image": processed_data_url,
            "filename": filename,
            "dimensions": {"width": w, "height": h},
            "execution_time_ms": elapsed_ms,
            "info": info
        })

    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Inpainting failed: {str(e)}"}), 500

# --- Dedicated Compression Endpoint (Practical 7) ---
@app.route("/api/compress", methods=["POST"])
def compress_image():
    start_time = time.perf_counter()
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image uploaded."}), 400

        file_obj = request.files["image"]
        img, _, byte_len = decode_image_file(file_obj)
        h, w = img.shape[:2]

        params_raw = request.form.get("params", "{}")
        try:
            params = json.loads(params_raw) if params_raw else {}
        except Exception:
            params = {}

        quality = int(params.get("quality", request.form.get("quality", 50)))
        params["quality"] = quality

        res_img, comp_data_url, info, filename = process_practical7(img, byte_len, params)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return jsonify({
            "success": True,
            "practical": 7,
            "operation": "compress",
            "processed_image": comp_data_url,
            "filename": filename,
            "dimensions": {"width": w, "height": h},
            "execution_time_ms": elapsed_ms,
            "info": info
        })

    except Exception as e:
        return jsonify({"success": False, "error": f"Compression failed: {str(e)}"}), 500

# --- Dedicated Detection Endpoint (Practical 9) ---
@app.route("/api/detect", methods=["POST"])
def detect_objects():
    start_time = time.perf_counter()
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image uploaded."}), 400

        file_obj = request.files["image"]
        img, _, _ = decode_image_file(file_obj)
        h, w = img.shape[:2]

        params_raw = request.form.get("params", "{}")
        try:
            params = json.loads(params_raw) if params_raw else {}
        except Exception:
            params = {}

        res_img, info, filename = process_practical9(img, "detect_object", params)
        processed_data_url, _ = encode_image_to_base64(res_img)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return jsonify({
            "success": True,
            "practical": 9,
            "operation": "detect_object",
            "processed_image": processed_data_url,
            "filename": filename,
            "dimensions": {"width": w, "height": h},
            "execution_time_ms": elapsed_ms,
            "info": info
        })

    except Exception as e:
        return jsonify({"success": False, "error": f"Detection failed: {str(e)}"}), 500

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  IMAGE PROCESSING LAB WEB APPLICATION — COLLEGE PRACTICALS (1–11)")
    print(f"  OpenCV Version: {cv2.__version__}")
    print("  Server running on: http://127.0.0.1:5000")
    print("="*70 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
