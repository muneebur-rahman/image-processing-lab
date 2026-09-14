import cv2
import numpy as np

def process_practical4(img, operation, params=None):
    """
    Practical 4: Spatial Domain Enhancement
    Operations:
      - contrast: cv2.convertScaleAbs(img, alpha=contrast, beta=0)
      - smooth: cv2.blur() or cv2.GaussianBlur()
      - sharpen: cv2.filter2D() with spatial kernel
      - threshold: cv2.threshold()
      - brightness: cv2.convertScaleAbs(img, alpha=1.0, beta=brightness)
    """
    if params is None:
        params = {}

    info = {"practical": 4, "operation": operation}

    if operation == "contrast":
        contrast_val = float(params.get("contrast", 1.5))  # alpha > 1 enhances contrast
        res = cv2.convertScaleAbs(img, alpha=contrast_val, beta=0)
        info["details"] = f"Adjusted contrast with gain factor alpha={contrast_val} using cv2.convertScaleAbs()."
        filename = f"practical4_contrast_a{contrast_val}.png"

    elif operation == "smooth":
        ksize = int(params.get("ksize", 5))
        if ksize % 2 == 0:
            ksize += 1
        ksize = max(1, min(ksize, 31))
        res = cv2.blur(img, (ksize, ksize))
        info["details"] = f"Applied spatial box smoothing with kernel size {ksize}x{ksize}."
        filename = f"practical4_smooth_k{ksize}.png"

    elif operation == "sharpen":
        ksize = int(params.get("ksize", 3))
        # High-pass / Laplacian sharpening kernel
        kernel = np.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ], dtype=np.float32)
        res = cv2.filter2D(img, -1, kernel)
        info["details"] = "Applied spatial domain 3x3 high-boost sharpening kernel via cv2.filter2D()."
        filename = "practical4_sharpen.png"

    elif operation == "threshold":
        thresh_val = int(params.get("threshold", 127))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img.copy()
        _, res = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
        info["details"] = f"Applied spatial binary threshold at intensity {thresh_val}."
        filename = f"practical4_threshold_{thresh_val}.png"

    elif operation == "brightness":
        brightness_val = float(params.get("brightness", 50))
        res = cv2.convertScaleAbs(img, alpha=1.0, beta=brightness_val)
        info["details"] = f"Applied spatial brightness bias beta={int(brightness_val):+d} via cv2.convertScaleAbs()."
        filename = f"practical4_brightness_{int(brightness_val)}.png"

    else:
        raise ValueError(f"Unknown operation for Practical 4: {operation}")

    return res, info, filename
