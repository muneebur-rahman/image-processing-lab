import cv2
import numpy as np

def process_practical6(img, operation, mask=None, params=None):
    """
    Practical 6: Image Inpainting
    Operations:
      - telea: cv2.inpaint(img, mask, inpaintRadius, cv2.INPAINT_TELEA)
      - navier_stokes: cv2.inpaint(img, mask, inpaintRadius, cv2.INPAINT_NS)
      - add_sample_scratch: generates a synthetic scratch and returns both marked image and mask for testing
    """
    if params is None:
        params = {}

    h, w = img.shape[:2]
    info = {"practical": 6, "operation": operation}
    radius = int(params.get("radius", 3))

    if operation == "add_sample_scratch":
        # Helpful utility to simulate image degradation (scratches / timestamp)
        marked_img = img.copy()
        generated_mask = np.zeros((h, w), dtype=np.uint8)
        # Draw a synthetic line and text scratch
        cv2.line(marked_img, (w // 5, h // 4), (4 * w // 5, 3 * h // 4), (255, 255, 255), 4)
        cv2.line(generated_mask, (w // 5, h // 4), (4 * w // 5, 3 * h // 4), 255, 4)
        cv2.putText(marked_img, "2026/09/14", (w // 4, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        cv2.putText(generated_mask, "2026/09/14", (w // 4, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 255, 3)
        info["details"] = "Synthesized sample scratches and date stamp onto the image to test inpainting algorithms."
        return marked_img, generated_mask, info, "practical6_simulated_scratch.png"

    if mask is None:
        raise ValueError("No inpainting mask provided. Please brush/mark the damaged area on the canvas first.")

    # Ensure mask dimensions match image
    if mask.shape[:2] != (h, w):
        mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)

    # Ensure mask is 8-bit single channel
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    _, mask_bin = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)

    # Ensure mask has non-zero pixels
    if cv2.countNonZero(mask_bin) == 0:
        raise ValueError("The inpainting mask is empty. Please draw on the image to mark the damaged pixels to restore.")

    if operation == "telea":
        res = cv2.inpaint(img, mask_bin, inpaintRadius=radius, flags=cv2.INPAINT_TELEA)
        info["details"] = f"Restored damaged area using Alexandru Telea's Fast Marching Method (cv2.INPAINT_TELEA, radius={radius})."
        filename = f"practical6_inpaint_telea_r{radius}.png"

    elif operation == "navier_stokes":
        res = cv2.inpaint(img, mask_bin, inpaintRadius=radius, flags=cv2.INPAINT_NS)
        info["details"] = f"Restored damaged area using Bertalmio et al. Navier-Stokes fluid dynamics method (cv2.INPAINT_NS, radius={radius})."
        filename = f"practical6_inpaint_navier_stokes_r{radius}.png"

    else:
        raise ValueError(f"Unknown operation for Practical 6: {operation}")

    return res, info, filename
