import cv2
import numpy as np

def process_practical8(img, operation, params=None):
    """
    Practical 8: Morphological Operations
    Operations:
      - binary: cv2.threshold() to create binary image
      - erosion: cv2.erode()
      - dilation: cv2.dilate()
      - opening: cv2.morphologyEx(..., cv2.MORPH_OPEN) (erosion followed by dilation)
      - closing: cv2.morphologyEx(..., cv2.MORPH_CLOSE) (dilation followed by erosion)
    """
    if params is None:
        params = {}

    info = {"practical": 8, "operation": operation}

    # Kernel configuration
    ksize = int(params.get("ksize", 5))
    if ksize % 2 == 0:
        ksize += 1
    ksize = max(1, min(ksize, 31))

    shape_name = params.get("shape", "rect")
    shape_map = {
        "rect": cv2.MORPH_RECT,
        "cross": cv2.MORPH_CROSS,
        "ellipse": cv2.MORPH_ELLIPSE
    }
    morph_shape = shape_map.get(shape_name, cv2.MORPH_RECT)
    kernel = cv2.getStructuringElement(morph_shape, (ksize, ksize))

    iterations = int(params.get("iterations", 1))
    iterations = max(1, min(iterations, 10))

    thresh_val = int(params.get("threshold", 127))
    use_binary = params.get("use_binary", True)

    if operation == "binary":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img.copy()
        _, res = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
        info["details"] = f"Generated binary threshold image at cutoff {thresh_val}."
        filename = f"practical8_binary_t{thresh_val}.png"
        return res, info, filename

    # For erosion, dilation, opening, closing
    # Standard practice: convert to binary if requested or work directly
    if use_binary:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img.copy()
        _, work_img = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    else:
        work_img = img.copy()

    if operation == "erosion":
        res = cv2.erode(work_img, kernel, iterations=iterations)
        info["details"] = f"Applied erosion with {shape_name} kernel ({ksize}x{ksize}) for {iterations} iteration(s) using cv2.erode()."
        filename = f"practical8_erosion_k{ksize}_i{iterations}.png"

    elif operation == "dilation":
        res = cv2.dilate(work_img, kernel, iterations=iterations)
        info["details"] = f"Applied dilation with {shape_name} kernel ({ksize}x{ksize}) for {iterations} iteration(s) using cv2.dilate()."
        filename = f"practical8_dilation_k{ksize}_i{iterations}.png"

    elif operation == "opening":
        res = cv2.morphologyEx(work_img, cv2.MORPH_OPEN, kernel, iterations=iterations)
        info["details"] = f"Applied Opening (Erosion followed by Dilation: removes noise/isolated foreground pixels) using cv2.morphologyEx()."
        filename = f"practical8_opening_k{ksize}.png"

    elif operation == "closing":
        res = cv2.morphologyEx(work_img, cv2.MORPH_CLOSE, kernel, iterations=iterations)
        info["details"] = f"Applied Closing (Dilation followed by Erosion: fills small holes and gaps) using cv2.morphologyEx()."
        filename = f"practical8_closing_k{ksize}.png"

    else:
        raise ValueError(f"Unknown operation for Practical 8: {operation}")

    return res, info, filename
