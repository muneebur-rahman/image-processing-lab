import cv2
import numpy as np

def process_practical10(img, operation="canny", params=None):
    """
    Practical 10: Edge Detection
    Primary Operation:
      - canny: cv2.Canny(gray, threshold1, threshold2, apertureSize, L2gradient)
    Optional Advanced Operators:
      - sobel: cv2.Sobel() (horizontal, vertical, or combined magnitude)
      - laplacian: cv2.Laplacian() second-order derivative
    """
    if params is None:
        params = {}

    info = {"practical": 10, "operation": operation}

    # Step 1: Grayscale conversion
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    # Step 2: Optional Gaussian pre-filtering to remove noise
    blur_ksize = int(params.get("blur_ksize", 3))
    if blur_ksize > 1:
        if blur_ksize % 2 == 0:
            blur_ksize += 1
        gray = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)

    if operation == "canny" or operation == "detect_edges":
        t1 = int(params.get("threshold1", 100))
        t2 = int(params.get("threshold2", 200))
        aperture = int(params.get("aperture", 3))
        if aperture not in (3, 5, 7):
            aperture = 3
        l2_grad = bool(params.get("l2_gradient", False))

        res = cv2.Canny(gray, threshold1=t1, threshold2=t2, apertureSize=aperture, L2gradient=l2_grad)
        info["details"] = f"Canny edge detector executed: threshold1={t1}, threshold2={t2}, aperture={aperture}, L2gradient={l2_grad}."
        filename = f"practical10_canny_{t1}_{t2}.png"

    elif operation == "sobel":
        direction = params.get("direction", "both")
        ksize = int(params.get("ksize", 3))
        if ksize not in (1, 3, 5, 7):
            ksize = 3

        if direction == "horizontal":
            sobel_raw = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
            res = cv2.convertScaleAbs(sobel_raw)
            info["details"] = f"Sobel Horizontal (dY) edge detection with ksize={ksize}."
        elif direction == "vertical":
            sobel_raw = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
            res = cv2.convertScaleAbs(sobel_raw)
            info["details"] = f"Sobel Vertical (dX) edge detection with ksize={ksize}."
        else:
            gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
            gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
            mag = cv2.magnitude(gx, gy)
            res = cv2.convertScaleAbs(mag)
            info["details"] = f"Sobel Combined Gradient Magnitude (dX + dY) with ksize={ksize}."
        filename = f"practical10_sobel_{direction}.png"

    elif operation == "laplacian":
        ksize = int(params.get("ksize", 3))
        if ksize not in (1, 3, 5, 7):
            ksize = 3
        lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
        res = cv2.convertScaleAbs(lap)
        info["details"] = f"Laplacian second-order spatial derivative with ksize={ksize}."
        filename = f"practical10_laplacian_k{ksize}.png"

    else:
        raise ValueError(f"Unknown operation for Practical 10: {operation}")

    return res, info, filename
