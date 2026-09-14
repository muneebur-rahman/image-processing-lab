import cv2
import numpy as np

def process_practical2(img, operation, params=None):
    """
    Practical 2: Geometric Transformation
    Operations:
      - translation: cv2.warpAffine() with translation matrix
      - rotation: cv2.getRotationMatrix2D() + cv2.warpAffine()
      - scaling: cv2.resize()
      - shearing: affine matrix with shear factors + cv2.warpAffine()
      - reflection: cv2.flip()
      - cropping: dynamic array slicing img[y:y+h, x:x+w]
    """
    if params is None:
        params = {}

    h, w = img.shape[:2]
    info = {"practical": 2, "operation": operation}

    if operation == "translation":
        tx = float(params.get("tx", 50))
        ty = float(params.get("ty", 30))
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        res = cv2.warpAffine(img, M, (w, h))
        info["details"] = f"Translated image by tx={tx}px, ty={ty}px using cv2.warpAffine()."
        filename = f"practical2_translation_{int(tx)}_{int(ty)}.png"

    elif operation == "rotation":
        angle = float(params.get("angle", 45))
        scale = float(params.get("scale", 1.0))
        center_x = float(params.get("center_x", w / 2))
        center_y = float(params.get("center_y", h / 2))
        M = cv2.getRotationMatrix2D((center_x, center_y), angle, scale)
        res = cv2.warpAffine(img, M, (w, h))
        info["details"] = f"Rotated image by {angle}° around ({center_x:.0f}, {center_y:.0f}) with scale={scale} using cv2.getRotationMatrix2D() & cv2.warpAffine()."
        filename = f"practical2_rotation_{int(angle)}deg.png"

    elif operation == "scaling":
        scale_pct = float(params.get("scale", 150)) / 100.0  # percentage, e.g. 150% = 1.5
        new_w = max(1, int(w * scale_pct))
        new_h = max(1, int(h * scale_pct))
        interp = cv2.INTER_CUBIC if scale_pct > 1.0 else cv2.INTER_AREA
        res = cv2.resize(img, (new_w, new_h), interpolation=interp)
        info["details"] = f"Scaled image to {new_w}x{new_h} ({scale_pct*100:.0f}%) using cv2.resize()."
        filename = f"practical2_scaling_{int(scale_pct*100)}pct.png"

    elif operation == "shearing":
        shx = float(params.get("shx", 0.2))
        shy = float(params.get("shy", 0.0))
        # Affine shear matrix: [x', y'] = [x + shx*y, y + shy*x]
        M = np.float32([[1, shx, 0], [shy, 1, 0]])
        # Compute bounding output size to avoid severe clipping
        out_w = int(w + abs(shx) * h)
        out_h = int(h + abs(shy) * w)
        res = cv2.warpAffine(img, M, (out_w, out_h))
        info["details"] = f"Applied affine shearing with shx={shx}, shy={shy} using cv2.warpAffine()."
        filename = f"practical2_shearing_{shx}_{shy}.png"

    elif operation == "reflection":
        # flipCode: 1 = horizontal, 0 = vertical, -1 = both
        mode = params.get("mode", "horizontal")
        if mode == "vertical":
            flip_code = 0
            label = "Vertical (axis 0)"
        elif mode == "both":
            flip_code = -1
            label = "Horizontal & Vertical (axis -1)"
        else:
            flip_code = 1
            label = "Horizontal (axis 1)"
        res = cv2.flip(img, flip_code)
        info["details"] = f"Reflected image along {label} using cv2.flip(img, {flip_code})."
        filename = f"practical2_reflection_{mode}.png"

    elif operation == "cropping":
        # Fraction or pixel coords
        x = int(params.get("crop_x", w * 0.15))
        y = int(params.get("crop_y", h * 0.15))
        cw = int(params.get("crop_w", w * 0.70))
        ch = int(params.get("crop_h", h * 0.70))
        
        # Clamp bounds
        x = max(0, min(x, w - 1))
        y = max(0, min(y, h - 1))
        cw = max(10, min(cw, w - x))
        ch = max(10, min(ch, h - y))
        
        res = img[y:y+ch, x:x+cw]
        info["details"] = f"Dynamically cropped region (x={x}, y={y}, w={cw}, h={ch}) via NumPy array slicing img[y:y+h, x:x+w]."
        filename = f"practical2_crop_{x}_{y}_{cw}x{ch}.png"

    else:
        raise ValueError(f"Unknown operation for Practical 2: {operation}")

    return res, info, filename
