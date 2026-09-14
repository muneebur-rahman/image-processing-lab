import cv2
import numpy as np

def process_practical1(img, operation, params=None, second_img=None):
    """
    Practical 1: Image Basics & Arithmetic Operations
    Operations:
      - rgb_to_gray: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      - brightness: pixel arithmetic with overflow protection via cv2.convertScaleAbs
      - bitwise_not: cv2.bitwise_not(img)
      - bitwise_and: cv2.bitwise_and(img1, img2)
      - bitwise_or: cv2.bitwise_or(img1, img2)
    """
    if params is None:
        params = {}
    
    info = {"practical": 1, "operation": operation}
    h, w = img.shape[:2]

    if operation == "rgb_to_gray":
        if len(img.shape) == 2 or img.shape[2] == 1:
            res = img.copy()
        else:
            res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        info["details"] = "Converted 3-channel BGR image to single-channel Grayscale using cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)."
        filename = "practical1_rgb_to_gray.png"

    elif operation == "brightness":
        brightness_val = float(params.get("brightness", 50))
        # cv2.convertScaleAbs prevents uint8 wrap-around / overflow
        res = cv2.convertScaleAbs(img, alpha=1.0, beta=brightness_val)
        info["details"] = f"Adjusted brightness by {int(brightness_val):+d} using cv2.convertScaleAbs(img, alpha=1.0, beta={brightness_val})."
        filename = f"practical1_brightness_{int(brightness_val)}.png"

    elif operation == "bitwise_not":
        res = cv2.bitwise_not(img)
        info["details"] = "Computed bitwise NOT (inversion: 255 - pixel) using cv2.bitwise_not(img)."
        filename = "practical1_bitwise_not.png"

    elif operation in ("bitwise_and", "bitwise_or"):
        # If second image is provided, match its shape to first image
        if second_img is not None:
            img2 = cv2.resize(second_img, (w, h))
            if len(img.shape) == 3 and len(img2.shape) == 2:
                img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
            elif len(img.shape) == 2 and len(img2.shape) == 3:
                img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        else:
            # Fallback: create a geometric circular aperture mask
            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.circle(mask, (w // 2, h // 2), min(w, h) // 3, 255, -1)
            if len(img.shape) == 3:
                img2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            else:
                img2 = mask

        if operation == "bitwise_and":
            res = cv2.bitwise_and(img, img2)
            info["details"] = "Performed bitwise AND using cv2.bitwise_and(). " + (
                "Applied with uploaded second image." if second_img is not None else "Applied with generated circular binary mask."
            )
            filename = "practical1_bitwise_and.png"
        else:
            res = cv2.bitwise_or(img, img2)
            info["details"] = "Performed bitwise OR using cv2.bitwise_or(). " + (
                "Applied with uploaded second image." if second_img is not None else "Applied with generated circular binary mask."
            )
            filename = "practical1_bitwise_or.png"

    else:
        raise ValueError(f"Unknown operation for Practical 1: {operation}")

    return res, info, filename
