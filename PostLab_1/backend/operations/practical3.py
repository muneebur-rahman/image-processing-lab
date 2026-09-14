import cv2
import numpy as np

def process_practical3(img, operation, params=None):
    """
    Practical 3: Image Enhancement
    Operations:
      - histogram_equalization: cv2.equalizeHist()
      - smoothing: cv2.GaussianBlur() or cv2.blur()
      - sharpening: cv2.filter2D() with sharpening kernel
      - thresholding: cv2.threshold() with interactive threshold parameters
    """
    if params is None:
        params = {}

    info = {"practical": 3, "operation": operation}

    if operation == "histogram_equalization":
        mode = params.get("mode", "color")  # "color" or "gray"
        if len(img.shape) == 2 or mode == "gray":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
            res = cv2.equalizeHist(gray)
            info["details"] = "Applied cv2.equalizeHist() on grayscale image to normalize illumination and enhance dynamic range."
            filename = "practical3_hist_equalization_gray.png"
        else:
            # Equalize luminance channel in YCrCb to preserve chromaticity
            ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            res = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
            info["details"] = "Converted to YCrCb colour space, equalized Y (luminance) channel with cv2.equalizeHist(), and converted back to BGR."
            filename = "practical3_hist_equalization_color.png"

    elif operation == "smoothing":
        ksize = int(params.get("ksize", 5))
        if ksize % 2 == 0:
            ksize += 1
        ksize = max(1, min(ksize, 31))
        
        filter_type = params.get("filter_type", "gaussian")
        if filter_type == "box":
            res = cv2.blur(img, (ksize, ksize))
            info["details"] = f"Applied box averaging filter cv2.blur(img, ({ksize}, {ksize}))."
            filename = f"practical3_smoothing_box_k{ksize}.png"
        else:
            sigma = float(params.get("sigma", 0))
            res = cv2.GaussianBlur(img, (ksize, ksize), sigmaX=sigma)
            info["details"] = f"Applied cv2.GaussianBlur(img, ({ksize}, {ksize}), sigmaX={sigma})."
            filename = f"practical3_smoothing_gaussian_k{ksize}.png"

    elif operation == "sharpening":
        strength = float(params.get("strength", 1.0))
        # Base kernel: center = 1 + 4*strength, neighbors = -strength
        center = 1.0 + 4.0 * strength
        kernel = np.array([
            [0, -strength, 0],
            [-strength, center, -strength],
            [0, -strength, 0]
        ], dtype=np.float32)
        res = cv2.filter2D(img, -1, kernel)
        info["details"] = f"Applied 2D spatial sharpening filter cv2.filter2D() with center weight {center:.1f}."
        filename = f"practical3_sharpening_s{strength}.png"

    elif operation == "thresholding":
        thresh_val = int(params.get("threshold", 127))
        thresh_type_name = params.get("type", "binary")
        
        # Convert to grayscale first
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img.copy()
        
        type_map = {
            "binary": cv2.THRESH_BINARY,
            "binary_inv": cv2.THRESH_BINARY_INV,
            "trunc": cv2.THRESH_TRUNC,
            "tozero": cv2.THRESH_TOZERO,
            "tozero_inv": cv2.THRESH_TOZERO_INV,
            "otsu": cv2.THRESH_BINARY + cv2.THRESH_OTSU
        }
        cv_type = type_map.get(thresh_type_name, cv2.THRESH_BINARY)
        
        ret, res = cv2.threshold(gray, thresh_val, 255, cv_type)
        info["details"] = f"Applied cv2.threshold() with type '{thresh_type_name}', threshold={ret:.0f}, maxval=255."
        filename = f"practical3_threshold_{thresh_type_name}_{int(ret)}.png"

    else:
        raise ValueError(f"Unknown operation for Practical 3: {operation}")

    return res, info, filename
