import base64
import os
import cv2
import numpy as np

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def is_allowed_file(filename):
    """Check if the filename has an allowed image extension."""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def decode_image_from_bytes(raw_bytes):
    """
    Decode image raw bytes into an OpenCV numpy array (BGR).
    Raises ValueError if decoding fails.
    """
    if not raw_bytes:
        raise ValueError("Empty image data received.")
    
    nparr = np.frombuffer(raw_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode image. File may be corrupted or unsupported format.")
    return img

def decode_image_file(file_storage):
    """Decode a Flask FileStorage object into an OpenCV image."""
    if file_storage is None or file_storage.filename == '':
        raise ValueError("No file uploaded.")
    
    if not is_allowed_file(file_storage.filename):
        raise ValueError(f"Invalid file extension. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}")
    
    raw_bytes = file_storage.read()
    return decode_image_from_bytes(raw_bytes), file_storage.filename, len(raw_bytes)

def encode_image_to_base64(img, ext='.png', quality=None):
    """
    Encode an OpenCV image (BGR or Grayscale) to a base64 data URL string.
    Returns (data_url, byte_size).
    """
    if img is None:
        raise ValueError("Cannot encode None image.")
    
    params = []
    if ext.lower() in ['.jpg', '.jpeg']:
        mime = 'image/jpeg'
        if quality is not None:
            params = [int(cv2.IMWRITE_JPEG_QUALITY), int(np.clip(quality, 1, 100))]
    elif ext.lower() == '.webp':
        mime = 'image/webp'
        if quality is not None:
            params = [int(cv2.IMWRITE_WEBP_QUALITY), int(np.clip(quality, 1, 100))]
    else:
        mime = 'image/png'
        ext = '.png'
        # Compression level for PNG (0 to 9)
        params = [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
    
    success, buffer = cv2.imencode(ext, img, params)
    if not success:
        raise RuntimeError("Failed to encode image to buffer.")
    
    byte_data = buffer.tobytes()
    b64_str = base64.b64encode(byte_data).decode('utf-8')
    data_url = f"data:{mime};base64,{b64_str}"
    return data_url, len(byte_data)

def decode_mask_from_base64(mask_data_url_or_b64, target_shape):
    """
    Decode a base64 image data URL (from canvas) into a single-channel 8-bit uint8 binary mask (0 or 255).
    target_shape: (height, width) or (height, width, channels)
    """
    if not mask_data_url_or_b64:
        raise ValueError("Mask data is empty.")
    
    if ',' in mask_data_url_or_b64:
        header, b64_str = mask_data_url_or_b64.split(',', 1)
    else:
        b64_str = mask_data_url_or_b64
    
    mask_bytes = base64.b64decode(b64_str)
    nparr = np.frombuffer(mask_bytes, np.uint8)
    
    # Read with alpha channel to detect drawn brush strokes
    mask_img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    if mask_img is None:
        raise ValueError("Failed to decode mask image.")
    
    h_target, w_target = target_shape[:2]
    # Resize mask to match original image dimensions if needed
    if mask_img.shape[0] != h_target or mask_img.shape[1] != w_target:
        mask_img = cv2.resize(mask_img, (w_target, h_target), interpolation=cv2.INTER_NEAREST)
    
    # Extract binary mask
    if mask_img.ndim == 3:
        if mask_img.shape[2] == 4:
            # Alpha channel > 20 means user painted here
            alpha = mask_img[:, :, 3]
            # Also check color channels (red brush or non-black)
            bgr = mask_img[:, :, :3]
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            binary_mask = np.where((alpha > 20) | (gray > 20), 255, 0).astype(np.uint8)
        else:
            gray = cv2.cvtColor(mask_img, cv2.COLOR_BGR2GRAY)
            _, binary_mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    else:
        _, binary_mask = cv2.threshold(mask_img, 20, 255, cv2.THRESH_BINARY)
    
    return binary_mask
