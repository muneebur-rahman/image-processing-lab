import os
import cv2
import numpy as np
import pytest

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

@pytest.fixture
def sample_bgr_image():
    """Create a 120x120 synthetic BGR test image."""
    img = np.zeros((120, 120, 3), dtype=np.uint8)
    cv2.rectangle(img, (20, 20), (80, 80), (0, 255, 255), -1)
    cv2.circle(img, (60, 60), 25, (255, 0, 128), -1)
    return img

@pytest.fixture
def sample_second_image():
    """Create a 120x120 synthetic secondary test image for bitwise ops."""
    img = np.zeros((120, 120, 3), dtype=np.uint8)
    cv2.circle(img, (60, 60), 40, (255, 255, 255), -1)
    return img

# --- Practical 1 Tests ---
def test_practical1_all_operations(sample_bgr_image, sample_second_image):
    for op in ["rgb_to_gray", "brightness", "bitwise_not", "bitwise_and", "bitwise_or"]:
        res, info, fn = process_practical1(sample_bgr_image, op, {"brightness": 40}, sample_second_image)
        assert res is not None
        assert isinstance(res, np.ndarray)
        assert fn.endswith(".png")
        assert info["practical"] == 1

# --- Practical 2 Tests ---
def test_practical2_all_operations(sample_bgr_image):
    ops = ["translation", "rotation", "scaling", "shearing", "reflection", "cropping"]
    for op in ops:
        res, info, fn = process_practical2(sample_bgr_image, op, {
            "tx": 10, "ty": 15, "angle": 30, "scale": 120, "shx": 0.2, "crop_x": 10, "crop_y": 10, "crop_w": 50, "crop_h": 50
        })
        assert res is not None
        assert res.size > 0
        assert info["practical"] == 2

# --- Practical 3 Tests ---
def test_practical3_all_operations(sample_bgr_image):
    ops = ["histogram_equalization", "smoothing", "sharpening", "thresholding"]
    for op in ops:
        res, info, fn = process_practical3(sample_bgr_image, op, {"threshold": 100, "strength": 1.2, "ksize": 5})
        assert res is not None
        assert info["practical"] == 3

# --- Practical 4 Tests ---
def test_practical4_all_operations(sample_bgr_image):
    ops = ["contrast", "smooth", "sharpen", "threshold", "brightness"]
    for op in ops:
        res, info, fn = process_practical4(sample_bgr_image, op, {"contrast": 1.5, "ksize": 5, "brightness": 30})
        assert res is not None
        assert info["practical"] == 4

# --- Practical 5 Tests ---
def test_practical5_all_operations(sample_bgr_image):
    ops = ["averaging", "gaussian", "median", "bilateral"]
    for op in ops:
        res, info, fn = process_practical5(sample_bgr_image, op, {"ksize": 5, "sigma": 1.5, "diameter": 5})
        assert res is not None
        assert info["practical"] == 5

# --- Practical 6 Tests ---
def test_practical6_inpainting(sample_bgr_image):
    # Test sample scratch generator
    scratched, mask, info, fn = process_practical6(sample_bgr_image, "add_sample_scratch")
    assert scratched is not None
    assert mask is not None
    
    # Test telea and navier-stokes with mask
    for op in ["telea", "navier_stokes"]:
        res, info, fn = process_practical6(scratched, op, mask, {"radius": 3})
        assert res is not None
        assert res.shape == sample_bgr_image.shape

# --- Practical 7 Tests ---
def test_practical7_compression(sample_bgr_image):
    orig_bytes = sample_bgr_image.size
    decompressed, data_url, info, fn = process_practical7(sample_bgr_image, orig_bytes, {"quality": 40})
    assert decompressed is not None
    assert "data:image/jpeg;base64," in data_url
    assert info["quality"] == 40
    assert info["compressed_size_bytes"] > 0
    assert fn.endswith(".jpg")

# --- Practical 8 Tests ---
def test_practical8_morphology(sample_bgr_image):
    ops = ["binary", "erosion", "dilation", "opening", "closing"]
    for op in ops:
        res, info, fn = process_practical8(sample_bgr_image, op, {"ksize": 5, "iterations": 1, "threshold": 120})
        assert res is not None
        assert info["practical"] == 8

# --- Practical 9 Tests ---
def test_practical9_detection(sample_bgr_image):
    for target in ["face", "eye"]:
        res, info, fn = process_practical9(sample_bgr_image, "detect_object", {"target": target, "min_neighbors": 1})
        assert res is not None
        assert "detected_count" in info
        assert info["practical"] == 9

# --- Practical 10 Tests ---
def test_practical10_edge_detection(sample_bgr_image):
    ops = ["canny", "sobel", "laplacian"]
    for op in ops:
        res, info, fn = process_practical10(sample_bgr_image, op, {"threshold1": 80, "threshold2": 160})
        assert res is not None
        assert info["practical"] == 10

# --- Practical 11 Tests ---
def test_practical11_colour_spaces(sample_bgr_image):
    for space in ["rgb", "gray", "hsv", "lab", "ycrcb"]:
        res, info, fn = process_practical11(sample_bgr_image, "convert", {"target_space": space, "split_channel": "all"})
        assert res is not None
        assert info["target_space"] == space.upper()
