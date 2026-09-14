import base64
import cv2
import numpy as np

def process_practical7(img, original_bytes_len, params=None):
    """
    Practical 7: Image Compression
    Operation:
      - compress: JPEG lossy compression with user-selected quality parameter (10-100)
    Calculates actual byte size, compressed byte size, and savings percentage.
    """
    if params is None:
        params = {}

    quality = int(params.get("quality", 50))
    quality = max(5, min(quality, 100))

    # Encode to JPEG buffer with specified quality factor
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    success, buffer = cv2.imencode(".jpg", img, encode_param)
    if not success:
        raise RuntimeError("Failed to compress image with OpenCV JPEG encoder.")

    compressed_bytes = buffer.tobytes()
    compressed_size = len(compressed_bytes)

    # Decode back for visualization in frontend
    decompressed_img = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

    # Calculate actual compression statistics
    # If original_bytes_len is available, use it; otherwise estimate from raw uncompressed BGR bytes
    orig_size = original_bytes_len if original_bytes_len > 0 else (img.shape[0] * img.shape[1] * img.shape[2])
    savings_pct = max(0.0, ((orig_size - compressed_size) / orig_size) * 100.0) if orig_size > 0 else 0.0
    comp_ratio = (orig_size / compressed_size) if compressed_size > 0 else 1.0

    b64_str = base64.b64encode(compressed_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{b64_str}"

    info = {
        "practical": 7,
        "operation": "compress",
        "quality": quality,
        "original_size_bytes": orig_size,
        "compressed_size_bytes": compressed_size,
        "original_size_kb": round(orig_size / 1024.0, 2),
        "compressed_size_kb": round(compressed_size / 1024.0, 2),
        "savings_percentage": round(savings_pct, 2),
        "compression_ratio": round(comp_ratio, 2),
        "details": f"JPEG lossy compression at Quality={quality}%. Reduced size from {orig_size/1024.0:.1f} KB to {compressed_size/1024.0:.1f} KB ({savings_pct:.1f}% reduction)."
    }

    filename = f"practical7_compressed_q{quality}.jpg"
    return decompressed_img, data_url, info, filename
