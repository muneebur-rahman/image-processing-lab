import cv2
import numpy as np

def process_practical11(img, operation="convert", params=None):
    """
    Practical 11: Colour Spaces
    Converts image between standard colour spaces:
      - RGB (converted from OpenCV BGR)
      - Grayscale: cv2.COLOR_BGR2GRAY
      - HSV: cv2.COLOR_BGR2HSV (Hue, Saturation, Value)
      - LAB: cv2.COLOR_BGR2LAB (Luminance, a* green-red, b* blue-yellow)
      - YCrCb: cv2.COLOR_BGR2YCrCb (Luminance Y, Chrominance Red Cr, Chrominance Blue Cb)
    Also supports splitting channels for educational visualization.
    """
    if params is None:
        params = {}

    space = params.get("target_space", "hsv").lower()
    split_channel = params.get("split_channel", "all")  # "all", "ch1", "ch2", "ch3"

    info = {
        "practical": 11,
        "operation": operation,
        "target_space": space.upper(),
        "split_channel": split_channel
    }

    # Ensure 3-channel input
    if len(img.shape) == 2:
        bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        bgr = img.copy()

    channel_names = []

    if space == "grayscale" or space == "gray":
        res = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        info["details"] = "Converted to single-channel Grayscale (Luminance Y = 0.299R + 0.587G + 0.114B) via cv2.COLOR_BGR2GRAY."
        filename = "practical11_space_grayscale.png"
        return res, info, filename

    elif space == "rgb":
        # OpenCV loads in BGR; RGB flips channels 0 and 2
        res = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        channel_names = ["Red", "Green", "Blue"]
        info["details"] = "Converted from OpenCV internal BGR order to standard RGB colour model via cv2.COLOR_BGR2RGB."

    elif space == "hsv":
        converted = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        channel_names = ["Hue (0-179)", "Saturation (0-255)", "Value (0-255)"]
        info["details"] = "Converted to HSV (Hue, Saturation, Value). Displays cylindrical coordinates of colour perception."
        res = converted

    elif space == "lab":
        converted = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
        channel_names = ["L* (Lightness 0-255)", "a* (Green to Red)", "b* (Blue to Yellow)"]
        info["details"] = "Converted to CIE L*a*b* colour space. L* encodes perceptual lightness, while a* and b* encode chromatic opponent dimensions."
        res = converted

    elif space in ("ycrcb", "yuv"):
        converted = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
        channel_names = ["Y (Luma)", "Cr (Chroma Red)", "Cb (Chroma Blue)"]
        info["details"] = "Converted to YCrCb colour space widely used in video broadcasting and JPEG compression."
        res = converted

    else:
        raise ValueError(f"Unsupported colour space: {space}")

    # Handle channel splitting if user selected a single component
    if split_channel in ("ch1", "ch2", "ch3"):
        ch_idx = 0 if split_channel == "ch1" else (1 if split_channel == "ch2" else 2)
        single_ch = res[:, :, ch_idx]
        ch_title = channel_names[ch_idx] if ch_idx < len(channel_names) else f"Channel {ch_idx+1}"
        info["details"] += f" Displaying isolated single channel: {ch_title}."
        filename = f"practical11_{space}_{split_channel}_{ch_title.split()[0].lower()}.png"
        return single_ch, info, filename

    filename = f"practical11_{space}_full.png"
    return res, info, filename
