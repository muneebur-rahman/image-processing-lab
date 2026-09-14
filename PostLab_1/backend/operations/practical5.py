import cv2
import numpy as np

def process_practical5(img, operation, params=None):
    """
    Practical 5: Spatial Filters
    Operations:
      - averaging: cv2.blur() / cv2.boxFilter()
      - gaussian: cv2.GaussianBlur()
      - median: cv2.medianBlur()
      - bilateral: cv2.bilateralFilter()
    """
    if params is None:
        params = {}

    info = {"practical": 5, "operation": operation}

    if operation == "averaging":
        ksize = int(params.get("ksize", 5))
        if ksize % 2 == 0:
            ksize += 1
        ksize = max(1, min(ksize, 31))
        res = cv2.blur(img, (ksize, ksize))
        info["details"] = f"Averaging / Box filter applied using cv2.blur(img, ({ksize}, {ksize}))."
        filename = f"practical5_averaging_k{ksize}.png"

    elif operation == "gaussian":
        ksize = int(params.get("ksize", 5))
        if ksize % 2 == 0:
            ksize += 1
        ksize = max(1, min(ksize, 31))
        sigma_x = float(params.get("sigma", 1.5))
        res = cv2.GaussianBlur(img, (ksize, ksize), sigmaX=sigma_x)
        info["details"] = f"Gaussian filter applied using cv2.GaussianBlur(img, ({ksize}, {ksize}), sigmaX={sigma_x})."
        filename = f"practical5_gaussian_k{ksize}_s{sigma_x}.png"

    elif operation == "median":
        ksize = int(params.get("ksize", 5))
        if ksize % 2 == 0:
            ksize += 1
        ksize = max(3, min(ksize, 31))  # medianBlur requires odd integer > 1
        res = cv2.medianBlur(img, ksize)
        info["details"] = f"Median filter (salt-and-pepper noise removal) applied using cv2.medianBlur(img, {ksize})."
        filename = f"practical5_median_k{ksize}.png"

    elif operation == "bilateral":
        d = int(params.get("diameter", 9))
        sigma_color = float(params.get("sigma_color", 75))
        sigma_space = float(params.get("sigma_space", 75))
        res = cv2.bilateralFilter(img, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)
        info["details"] = f"Edge-preserving Bilateral filter applied using cv2.bilateralFilter(img, d={d}, sigmaColor={sigma_color}, sigmaSpace={sigma_space})."
        filename = f"practical5_bilateral_d{d}.png"

    else:
        raise ValueError(f"Unknown operation for Practical 5: {operation}")

    return res, info, filename
