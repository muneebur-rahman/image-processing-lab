# Image Processing Lab — Interactive Web Application

An interactive, laboratory-grade web application built for the college **Image Processing Subject (5th Semester)**. Students and instructors can execute, explore, and analyze all 11 curriculum practicals directly through a clean, modern web interface powered by **real Python OpenCV (`cv2`) operations**.

---

## 🔬 Core Highlights

- **100% Real OpenCV Processing:** No fake or mock image outputs. Every uploaded image is decoded into a NumPy matrix and processed using authentic OpenCV computer vision algorithms.
- **Dynamic Image Support:** Supports **JPG, JPEG, PNG, and WEBP** images with drag-and-drop uploading and immediate preview.
- **Native Camera Capture:** Live browser camera stream via `navigator.mediaDevices.getUserMedia()` with one-click photo capture and retake support.
- **One-Click Direct Download:** Immediately downloads the currently displayed processed image with a semantic, descriptive filename (e.g. `practical1_rgb_to_gray.png`, `practical7_compressed_q35.jpg`).
- **Interactive Damage Inpainting Mask (Practical 6):** Includes an HTML5 canvas brush overlay enabling students to paint scratches directly onto photos to generate the exact binary mask used by `cv2.inpaint`.
- **Real-Time Compression Analytics (Practical 7):** Computes original byte size, compressed byte size, dynamic storage reduction percentage, and compression ratio.
- **Dual-Image Processing (Practical 1):** Provides an optional secondary image upload zone for Bitwise AND/OR operations with automatic dimension matching.
- **Preloaded Lab Samples:** Includes offline test images (Faces, Geometric Shapes, Landscapes, Scratched Photos) for instantaneous experimentation.

---

## 📚 Curriculum Practicals (1 to 11)

| Practical # | Practical Title | Operations & OpenCV Functions |
| :--- | :--- | :--- |
| **Practical 1** | **Image Basics & Arithmetic Operations** | `cv2.cvtColor()` (RGB to Gray), `cv2.convertScaleAbs()` (Brightness + with overflow protection), `cv2.bitwise_not()`, `cv2.bitwise_and()`, `cv2.bitwise_or()`. Supports dual-image uploads. |
| **Practical 2** | **Geometric Transformation** | `cv2.warpAffine()` (Translation & Shearing), `cv2.getRotationMatrix2D()` (Rotation & Scaling), `cv2.resize()`, `cv2.flip()` (Reflection), Dynamic NumPy ROI array slicing (Cropping). |
| **Practical 3** | **Image Enhancement** | `cv2.equalizeHist()` (Histogram Equalization for Gray & Color YCrCb), `cv2.GaussianBlur()` / `cv2.blur()` (Smoothing), `cv2.filter2D()` (Sharpening kernel), `cv2.threshold()` (Binary, Inv, Trunc, ToZero, Otsu). |
| **Practical 4** | **Spatial Domain Enhancement** | Contrast gain (`alpha`), Box smoothing (`ksize`), Spatial High-Boost Sharpening, Binary Thresholding, and Brightness bias (`beta`). |
| **Practical 5** | **Spatial Filters** | `cv2.blur()` (Averaging / Box Filter), `cv2.GaussianBlur()` (Gaussian Smoothing with $\sigma$), `cv2.medianBlur()` (Salt & Pepper Noise Removal), `cv2.bilateralFilter()` (Edge-Preserving Smoothing). |
| **Practical 6** | **Image Inpainting** | Interactive Canvas Masking, `cv2.inpaint(..., cv2.INPAINT_TELEA)` (Alexandru Telea Fast Marching Method), `cv2.inpaint(..., cv2.INPAINT_NS)` (Bertalmio Navier-Stokes Fluid Dynamics). |
| **Practical 7** | **Image Compression** | `cv2.imencode('.jpg', ...)` lossy JPEG compression with quality factor (10–100), real byte size reduction, and compression ratios. |
| **Practical 8** | **Morphological Operations** | `cv2.threshold()` (Binary Image), `cv2.erode()`, `cv2.dilate()`, `cv2.morphologyEx(..., cv2.MORPH_OPEN)` (Opening), `cv2.morphologyEx(..., cv2.MORPH_CLOSE)` (Closing) with Rectangular, Cross, and Elliptical structuring elements. |
| **Practical 9** | **Object Detection** | OpenCV Haar Feature-based Cascade Classifiers (`cv2.CascadeClassifier`) for Frontal Faces, Human Eyes, Smiles, and Pedestrians with bounding boxes and counts. |
| **Practical 10** | **Edge Detection** | `cv2.Canny()` with hysteresis thresholds ($T_1, T_2$), Gaussian pre-blur, `cv2.Sobel()` (dX, dY, and Gradient Magnitude), and `cv2.Laplacian()`. |
| **Practical 11** | **Colour Spaces** | `cv2.cvtColor()` conversions across RGB, Grayscale, HSV (Hue, Saturation, Value), CIE LAB ($L^*, a^*, b^*$), and YCrCb with optional individual channel isolation. |

---

## 🛠️ Technology Stack

- **Backend:** Python 3.10+ / 3.13, Flask, OpenCV (`cv2`), NumPy, Pillow
- **Frontend:** HTML5, Modern CSS3 (Laboratory Dark Mode, Glassmorphism, Responsive Grid), Vanilla JavaScript (ES6)
- **Cascades & Samples:** Bundled locally in `backend/cascades/` and `static/samples/` for 100% offline functionality.

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure Python 3.10 or higher is installed on your system.

### 2. Install Dependencies
Open your terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Start the Web Server
Launch the Flask application:
```bash
python app.py
```

### 4. Open in Browser
Visit the application in your web browser at:
```text
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests

Run the comprehensive pytest suite verifying all 11 practicals and backend API routes:
```bash
python -m pytest -v
```

---

## 📂 Project Structure

```text
PostLab_1/
├── app.py                      # Flask Server & API routing
├── requirements.txt            # Python dependencies
├── README.md                   # Lab documentation & guide
├── backend/
│   ├── __init__.py
│   ├── utils.py                # Image decoding, validation, base64 encoding
│   ├── cascades/               # Local Haar Cascade XML files (Face, Eye, Smile, Body)
│   └── operations/
│       ├── __init__.py
│       ├── practical1.py       # Basics & Arithmetic (RGB to Gray, Brightness, Bitwise)
│       ├── practical2.py       # Geometric Transformations (Translate, Rotate, Scale, Shear, Flip, Crop)
│       ├── practical3.py       # Image Enhancement (Hist Eq, Smooth, Sharpen, Threshold)
│       ├── practical4.py       # Spatial Domain Enhancement
│       ├── practical5.py       # Spatial Filters (Box, Gaussian, Median, Bilateral)
│       ├── practical6.py       # Inpainting (Telea & Navier-Stokes with Canvas Mask)
│       ├── practical7.py       # JPEG Compression & Size Metrics
│       ├── practical8.py       # Morphological Ops (Binary, Erode, Dilate, Open, Close)
│       ├── practical9.py       # Object Detection (Haar Cascades)
│       ├── practical10.py      # Edge Detection (Canny, Sobel, Laplacian)
│       └── practical11.py      # Colour Spaces (RGB, Gray, HSV, LAB, YCrCb)
├── frontend/
│   ├── index.html              # Main Lab Web UI
│   ├── style.css               # Modern dark-mode lab styling
│   └── script.js               # Reactive frontend logic, canvas brush, download handler
├── static/
│   └── samples/                # Lab test sample images (shapes, scenery, face, scratched)
└── tests/
    ├── test_operations.py      # Unit tests for all 11 practical modules
    └── test_api.py             # Flask API integration tests
```

---

## 🎓 Academic Lab Usage Workflow

1. Open **Home** and click **Open Practical** on any practical card.
2. Click **Load Lab Sample** or **drag and drop** your own photograph.
3. Select an **Operation** tab (e.g., *Canny Edge Detection*, *Gaussian Blur*, *Telea Inpainting*).
4. Tune parameters using interactive sliders (e.g. *Kernel Size*, *Thresholds*, *Quality*).
5. Click **Process Image** to run the OpenCV algorithm on the server.
6. Inspect the side-by-side comparison and runtime metrics.
7. Click **Download Result** for instant, one-click saving of the generated image.

---

## 👨‍💻 Developer Credit

**Developed by Muneebur Rahman**  
B.Tech CSE | S. B. Jain Institute of Technology, Management & Research  
*Interactive Image Processing Lab using Python, OpenCV and Flask*
