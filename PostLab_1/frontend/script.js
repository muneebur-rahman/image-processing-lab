/* ==========================================================================
   IMAGE PROCESSING LAB — FRONTEND REACTIVE LOGIC
   Handles: Practicals navigation, dynamic controls, canvas inpaint masking,
            OpenCV API dispatching, side-by-side visualizer, and one-click download.
   ========================================================================== */

// --- Comprehensive Practicals Curriculum Definition ---
const PRACTICALS_DATA = [
  {
    id: 1,
    number: "Practical 1",
    title: "Image Basics & Arithmetic Operations",
    icon: "fa-palette",
    sampleImage: "static/samples/shapes.png",
    sampleImage2: "static/samples/scenery.jpg",
    desc: "Perform essential color conversions and mathematical pixel arithmetic using OpenCV.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.cvtColor()</code>, <code>cv2.convertScaleAbs()</code>, <code>cv2.bitwise_not()</code>, <code>cv2.bitwise_and()</code>, <code>cv2.bitwise_or()</code>.</p>
      <p><strong>Mathematical Concept:</strong> Grayscale conversion calculates luminance: $Y = 0.299R + 0.587G + 0.114B$. Brightness modification applies an additive bias $I'(x,y) = I(x,y) + \\beta$, saturated to $[0, 255]$. Bitwise operations perform boolean logic per bit plane.</p>
    `,
    operations: [
      { id: "rgb_to_gray", label: "RGB to Gray", icon: "fa-circle-half-stroke", params: [] },
      { id: "brightness", label: "Brightness +", icon: "fa-sun", params: [
        { id: "brightness", label: "Brightness Offset (Beta)", type: "slider", min: -100, max: 100, default: 50, step: 1, unit: "" }
      ]},
      { id: "bitwise_not", label: "Bitwise NOT", icon: "fa-yin-yang", params: [] },
      { id: "bitwise_and", label: "Bitwise AND", icon: "fa-circle-dot", params: [], needsSecondImage: true },
      { id: "bitwise_or", label: "Bitwise OR", icon: "fa-circle-notch", params: [], needsSecondImage: true }
    ]
  },
  {
    id: 2,
    number: "Practical 2",
    title: "Geometric Transformation",
    icon: "fa-vector-square",
    sampleImage: "static/samples/shapes.png",
    desc: "Transform spatial coordinate geometry: Translation, Rotation, Scaling, Shearing, Reflection & Cropping.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.warpAffine()</code>, <code>cv2.getRotationMatrix2D()</code>, <code>cv2.resize()</code>, <code>cv2.flip()</code>.</p>
      <p><strong>Mathematical Concept:</strong> Affine transformations map parallel lines to parallel lines via a $2\\times3$ matrix $[x', y']^T = A \\cdot [x, y]^T + B$. Cropping dynamically slices regions of interest (ROI) via NumPy array bounds.</p>
    `,
    operations: [
      { id: "translation", label: "Translation", icon: "fa-arrows-up-down-left-right", params: [
        { id: "tx", label: "Shift X (px)", type: "slider", min: -200, max: 200, default: 60, step: 5, unit: "px" },
        { id: "ty", label: "Shift Y (px)", type: "slider", min: -200, max: 200, default: 40, step: 5, unit: "px" }
      ]},
      { id: "rotation", label: "Rotation", icon: "fa-rotate", params: [
        { id: "angle", label: "Rotation Angle (°)", type: "slider", min: -180, max: 180, default: 45, step: 1, unit: "°" },
        { id: "scale", label: "Scale Factor", type: "slider", min: 0.2, max: 2.0, default: 1.0, step: 0.05, unit: "x" }
      ]},
      { id: "scaling", label: "Scaling", icon: "fa-up-right-and-down-left-from-center", params: [
        { id: "scale", label: "Resize Scale (%)", type: "slider", min: 20, max: 250, default: 140, step: 5, unit: "%" }
      ]},
      { id: "shearing", label: "Shearing", icon: "fa-shapes", params: [
        { id: "shx", label: "Shear X (Horizontal)", type: "slider", min: -0.8, max: 0.8, default: 0.3, step: 0.05, unit: "" },
        { id: "shy", label: "Shear Y (Vertical)", type: "slider", min: -0.8, max: 0.8, default: 0.0, step: 0.05, unit: "" }
      ]},
      { id: "reflection", label: "Reflection", icon: "fa-arrows-split-up-and-left", params: [
        { id: "mode", label: "Flip Axis", type: "select", options: [
          { value: "horizontal", label: "Horizontal (Around Y-axis)" },
          { value: "vertical", label: "Vertical (Around X-axis)" },
          { value: "both", label: "Both Axes (180° Inversion)" }
        ], default: "horizontal" }
      ]},
      { id: "cropping", label: "Cropping", icon: "fa-crop", params: [
        { id: "crop_x", label: "Region X Start (px)", type: "number", min: 0, default: 50 },
        { id: "crop_y", label: "Region Y Start (px)", type: "number", min: 0, default: 50 },
        { id: "crop_w", label: "Crop Width (px)", type: "number", min: 10, default: 300 },
        { id: "crop_h", label: "Crop Height (px)", type: "number", min: 10, default: 300 }
      ]}
    ]
  },
  {
    id: 3,
    number: "Practical 3",
    title: "Image Enhancement",
    icon: "fa-wand-magic-sparkles",
    sampleImage: "static/samples/scenery.jpg",
    desc: "Histogram Equalization, Spatial Smoothing, Sharpening, and Adaptive Thresholding.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.equalizeHist()</code>, <code>cv2.GaussianBlur()</code>, <code>cv2.filter2D()</code>, <code>cv2.threshold()</code>.</p>
      <p><strong>Mathematical Concept:</strong> Histogram Equalization flattens the probability density function (PDF) of pixel intensities, maximizing contrast. Sharpening amplifies high-frequency gradient information via discrete convolution.</p>
    `,
    operations: [
      { id: "histogram_equalization", label: "Histogram Equalization", icon: "fa-chart-column", params: [
        { id: "mode", label: "Channel Mode", type: "select", options: [
          { value: "color", label: "Color (YCrCb Luminance Equalized)" },
          { value: "gray", label: "Grayscale Equalization" }
        ], default: "color" }
      ]},
      { id: "smoothing", label: "Smoothing", icon: "fa-water", params: [
        { id: "filter_type", label: "Filter Type", type: "select", options: [
          { value: "gaussian", label: "Gaussian Blur" },
          { value: "box", label: "Box Averaging Blur" }
        ], default: "gaussian" },
        { id: "ksize", label: "Kernel Size (Odd)", type: "slider", min: 3, max: 25, default: 7, step: 2, unit: "px" },
        { id: "sigma", label: "Gaussian Sigma", type: "slider", min: 0, max: 10, default: 1.5, step: 0.5, unit: "" }
      ]},
      { id: "sharpening", label: "Sharpening", icon: "fa-feather", params: [
        { id: "strength", label: "Sharpening Intensity", type: "slider", min: 0.5, max: 4.0, default: 1.5, step: 0.25, unit: "x" }
      ]},
      { id: "thresholding", label: "Thresholding", icon: "fa-circle-half-stroke", params: [
        { id: "type", label: "Threshold Algorithm", type: "select", options: [
          { value: "binary", label: "cv2.THRESH_BINARY" },
          { value: "binary_inv", label: "cv2.THRESH_BINARY_INV" },
          { value: "trunc", label: "cv2.THRESH_TRUNC" },
          { value: "tozero", label: "cv2.THRESH_TOZERO" },
          { value: "otsu", label: "Otsu's Automatic Optimal Threshold" }
        ], default: "binary" },
        { id: "threshold", label: "Threshold Cutoff Value", type: "slider", min: 0, max: 255, default: 128, step: 1, unit: "" }
      ]}
    ]
  },
  {
    id: 4,
    number: "Practical 4",
    title: "Spatial Domain Enhancement",
    icon: "fa-sliders",
    sampleImage: "static/samples/scenery.jpg",
    desc: "Manipulate pixel values directly in the spatial coordinate domain (Contrast, Smooth, Sharpen, Threshold, Brightness).",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.convertScaleAbs()</code>, <code>cv2.blur()</code>, <code>cv2.filter2D()</code>, <code>cv2.threshold()</code>.</p>
      <p><strong>Mathematical Concept:</strong> Linear transformation model: $g(x,y) = \\alpha \\cdot f(x,y) + \\beta$, where $\\alpha$ controls contrast and $\\beta$ controls brightness. Spatial high-pass filters compute local Laplacian differences.</p>
    `,
    operations: [
      { id: "contrast", label: "Contrast", icon: "fa-circle-half-stroke", params: [
        { id: "contrast", label: "Contrast Factor (Alpha)", type: "slider", min: 0.5, max: 3.0, default: 1.8, step: 0.1, unit: "x" }
      ]},
      { id: "smooth", label: "Smooth", icon: "fa-water", params: [
        { id: "ksize", label: "Kernel Size (Odd)", type: "slider", min: 3, max: 25, default: 9, step: 2, unit: "px" }
      ]},
      { id: "sharpen", label: "Sharpen", icon: "fa-feather", params: [] },
      { id: "threshold", label: "Threshold", icon: "fa-bars-staggered", params: [
        { id: "threshold", label: "Intensity Cutoff", type: "slider", min: 0, max: 255, default: 120, step: 1, unit: "" }
      ]},
      { id: "brightness", label: "Apply Brightness", icon: "fa-sun", params: [
        { id: "brightness", label: "Brightness Value (Beta)", type: "slider", min: -100, max: 100, default: 50, step: 1, unit: "" }
      ]}
    ]
  },
  {
    id: 5,
    number: "Practical 5",
    title: "Spatial Filters",
    icon: "fa-filter",
    sampleImage: "static/samples/scenery.jpg",
    desc: "Apply 2D spatial convolution masks: Averaging, Gaussian, Median, and Bilateral Filters.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.blur()</code>, <code>cv2.GaussianBlur()</code>, <code>cv2.medianBlur()</code>, <code>cv2.bilateralFilter()</code>.</p>
      <p><strong>Mathematical Concept:</strong> Spatial filtering computes neighborhood weighted sums. Median filter non-linearly replaces center pixel with neighborhood median (ideal for impulse salt-and-pepper noise). Bilateral filter preserves sharp edges by combining spatial distance with color radiometric similarity.</p>
    `,
    operations: [
      { id: "averaging", label: "Averaging (Box)", icon: "fa-square", params: [
        { id: "ksize", label: "Kernel Size (Odd)", type: "slider", min: 3, max: 25, default: 7, step: 2, unit: "px" }
      ]},
      { id: "gaussian", label: "Gaussian", icon: "fa-mountain-sun", params: [
        { id: "ksize", label: "Kernel Size (Odd)", type: "slider", min: 3, max: 25, default: 7, step: 2, unit: "px" },
        { id: "sigma", label: "Standard Deviation (SigmaX)", type: "slider", min: 0.1, max: 10.0, default: 2.0, step: 0.2, unit: "" }
      ]},
      { id: "median", label: "Median", icon: "fa-grip", params: [
        { id: "ksize", label: "Aperture Linear Size (Odd)", type: "slider", min: 3, max: 25, default: 7, step: 2, unit: "px" }
      ]},
      { id: "bilateral", label: "Bilateral", icon: "fa-shield-halved", params: [
        { id: "diameter", label: "Pixel Neighborhood Diameter", type: "slider", min: 3, max: 21, default: 9, step: 2, unit: "px" },
        { id: "sigma_color", label: "Sigma Color (Range)", type: "slider", min: 10, max: 150, default: 75, step: 5, unit: "" },
        { id: "sigma_space", label: "Sigma Space (Coordinate)", type: "slider", min: 10, max: 150, default: 75, step: 5, unit: "" }
      ]}
    ]
  },
  {
    id: 6,
    number: "Practical 6",
    title: "Image Inpainting",
    icon: "fa-brush",
    sampleImage: "static/samples/scratched.png",
    desc: "Restore degraded or damaged photographs by painting a defect mask and reconstructing pixels.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.inpaint(img, inpaintMask, inpaintRadius, flags)</code> with <code>cv2.INPAINT_TELEA</code> and <code>cv2.INPAINT_NS</code>.</p>
      <p><strong>Mathematical Concept:</strong> Inpainting solves partial differential equations (PDEs) to smoothly propagate gradient contours from boundary known regions into missing/damaged zones. Telea uses the Fast Marching Method (FMM); Navier-Stokes treats pixel brightness like fluid streamlines.</p>
    `,
    operations: [
      { id: "telea", label: "Telea Inpainting", icon: "fa-wand-sparkles", params: [
        { id: "radius", label: "Inpainting Neighborhood Radius", type: "slider", min: 1, max: 15, default: 4, step: 1, unit: "px" }
      ], isInpaint: true },
      { id: "navier_stokes", label: "Navier-Stokes Inpainting", icon: "fa-water", params: [
        { id: "radius", label: "Inpainting Neighborhood Radius", type: "slider", min: 1, max: 15, default: 4, step: 1, unit: "px" }
      ], isInpaint: true }
    ]
  },
  {
    id: 7,
    number: "Practical 7",
    title: "Image Compression",
    icon: "fa-file-zipper",
    sampleImage: "static/samples/scenery.jpg",
    desc: "Analyze lossy JPEG image compression, dynamic file size reduction, and compression ratios.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])</code>.</p>
      <p><strong>Mathematical Concept:</strong> JPEG uses Discrete Cosine Transform (DCT) on $8\\times8$ pixel blocks, followed by psycho-visual quantization matrix scaling and Huffman entropy encoding. Lower quality factors quantize high-frequency coefficients more aggressively, yielding dramatic byte size savings with minor perceptual loss.</p>
    `,
    operations: [
      { id: "compress", label: "Compress Image", icon: "fa-compress", params: [
        { id: "quality", label: "JPEG Quality Factor (10–100)", type: "slider", min: 10, max: 100, default: 35, step: 5, unit: "%" }
      ], isCompression: true }
    ]
  },
  {
    id: 8,
    number: "Practical 8",
    title: "Morphological Operations",
    icon: "fa-cubes",
    sampleImage: "static/samples/shapes.png",
    desc: "Binary Image thresholding, Erosion, Dilation, Opening, and Closing using structuring elements.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.erode()</code>, <code>cv2.dilate()</code>, <code>cv2.morphologyEx()</code>, <code>cv2.getStructuringElement()</code>.</p>
      <p><strong>Mathematical Concept:</strong> Morphology analyzes geometric structures via set operations. <strong>Erosion</strong> ($A \\ominus B$) shrinks foreground boundaries and eliminates tiny noise. <strong>Dilation</strong> ($A \\oplus B$) expands boundaries and bridges gaps. <strong>Opening</strong> = Erosion $\\to$ Dilation (cleans background noise). <strong>Closing</strong> = Dilation $\\to$ Erosion (fills interior holes).</p>
    `,
    operations: [
      { id: "binary", label: "Binary Image", icon: "fa-toggle-on", params: [
        { id: "threshold", label: "Binary Threshold Value", type: "slider", min: 0, max: 255, default: 127, step: 1, unit: "" }
      ]},
      { id: "erosion", label: "Erosion", icon: "fa-compress", params: [
        { id: "ksize", label: "Kernel Size", type: "slider", min: 3, max: 21, default: 5, step: 2, unit: "px" },
        { id: "shape", label: "Structuring Element", type: "select", options: [
          { value: "rect", label: "Rectangle (cv2.MORPH_RECT)" },
          { value: "cross", label: "Cross (cv2.MORPH_CROSS)" },
          { value: "ellipse", label: "Ellipse (cv2.MORPH_ELLIPSE)" }
        ], default: "rect" },
        { id: "iterations", label: "Iterations", type: "slider", min: 1, max: 6, default: 1, step: 1, unit: "x" }
      ]},
      { id: "dilation", label: "Dilation", icon: "fa-expand", params: [
        { id: "ksize", label: "Kernel Size", type: "slider", min: 3, max: 21, default: 5, step: 2, unit: "px" },
        { id: "shape", label: "Structuring Element", type: "select", options: [
          { value: "rect", label: "Rectangle" },
          { value: "cross", label: "Cross" },
          { value: "ellipse", label: "Ellipse" }
        ], default: "rect" },
        { id: "iterations", label: "Iterations", type: "slider", min: 1, max: 6, default: 1, step: 1, unit: "x" }
      ]},
      { id: "opening", label: "Opening (Erode → Dilate)", icon: "fa-soap", params: [
        { id: "ksize", label: "Kernel Size", type: "slider", min: 3, max: 21, default: 5, step: 2, unit: "px" }
      ]},
      { id: "closing", label: "Closing (Dilate → Erode)", icon: "fa-fill", params: [
        { id: "ksize", label: "Kernel Size", type: "slider", min: 3, max: 21, default: 5, step: 2, unit: "px" }
      ]}
    ]
  },
  {
    id: 9,
    number: "Practical 9",
    title: "Object Detection",
    icon: "fa-crosshairs",
    sampleImage: "static/samples/face.png",
    desc: "Detect visual objects and faces locally using OpenCV Haar Feature-based Cascade Classifiers.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.CascadeClassifier()</code>, <code>detectMultiScale()</code>, <code>cv2.rectangle()</code>.</p>
      <p><strong>Mathematical Concept:</strong> Proposed by Viola and Jones, Haar cascades compute integral image rectangular features at various scales. An AdaBoost ensemble rapidly rejects non-object candidate windows, localizing target features (e.g. human eyes and frontal faces) in real time.</p>
    `,
    operations: [
      { id: "detect_object", label: "Detect Object", icon: "fa-user-check", params: [
        { id: "target", label: "Target Classifier", type: "select", options: [
          { value: "face", label: "Frontal Face Detector" },
          { value: "eye", label: "Human Eyes Detector" },
          { value: "smile", label: "Smile Detector" },
          { value: "fullbody", label: "Pedestrian / Full Body Detector" }
        ], default: "face" },
        { id: "scale_factor", label: "Scale Factor (Window Scale)", type: "slider", min: 1.05, max: 1.40, default: 1.10, step: 0.05, unit: "" },
        { id: "min_neighbors", label: "Min Neighbors (Strictness)", type: "slider", min: 1, max: 10, default: 3, step: 1, unit: "" }
      ], isDetection: true }
    ]
  },
  {
    id: 10,
    number: "Practical 10",
    title: "Edge Detection",
    icon: "fa-bezier-curve",
    sampleImage: "static/samples/scenery.jpg",
    desc: "Multi-stage Canny Edge Detector with hysteresis thresholding and gradient derivatives.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.Canny()</code>, <code>cv2.Sobel()</code>, <code>cv2.Laplacian()</code>.</p>
      <p><strong>Mathematical Concept:</strong> Canny operates in 4 rigorous steps: 1) Gaussian smoothing to suppress noise; 2) Gradient magnitude & direction calculation via Sobel; 3) Non-maximum suppression to thin edges; 4) Hysteresis thresholding ($T_1, T_2$) to retain strong edges and connected weak edges.</p>
    `,
    operations: [
      { id: "canny", label: "Canny Edge Detection", icon: "fa-draw-polygon", params: [
        { id: "threshold1", label: "Min Threshold (T1)", type: "slider", min: 10, max: 250, default: 100, step: 5, unit: "" },
        { id: "threshold2", label: "Max Threshold (T2)", type: "slider", min: 20, max: 300, default: 200, step: 5, unit: "" },
        { id: "blur_ksize", label: "Gaussian Pre-blur Kernel", type: "slider", min: 1, max: 11, default: 3, step: 2, unit: "px" }
      ]},
      { id: "sobel", label: "Sobel Gradient", icon: "fa-lines-leaning", params: [
        { id: "direction", label: "Gradient Direction", type: "select", options: [
          { value: "both", label: "Combined Magnitude (dX + dY)" },
          { value: "horizontal", label: "Horizontal Edges (dY)" },
          { value: "vertical", label: "Vertical Edges (dX)" }
        ], default: "both" },
        { id: "ksize", label: "Sobel Aperture Size", type: "select", options: [
          { value: 1, label: "1x1 (Fast)" },
          { value: 3, label: "3x3 (Standard)" },
          { value: 5, label: "5x5" }
        ], default: 3 }
      ]},
      { id: "laplacian", label: "Laplacian Derivative", icon: "fa-circle-notch", params: [
        { id: "ksize", label: "Aperture Size", type: "select", options: [
          { value: 1, label: "1x1" },
          { value: 3, label: "3x3" },
          { value: 5, label: "5x5" }
        ], default: 3 }
      ]}
    ]
  },
  {
    id: 11,
    number: "Practical 11",
    title: "Colour Spaces",
    icon: "fa-gem",
    sampleImage: "static/samples/shapes.png",
    desc: "Inter-conversion between RGB, Grayscale, HSV, LAB, and YCrCb colour spaces with channel analysis.",
    theory: `
      <p><strong>OpenCV Functions:</strong> <code>cv2.cvtColor()</code> with <code>cv2.COLOR_BGR2*</code>.</p>
      <p><strong>Mathematical Concept:</strong> Colour representations separate chromatic information from illumination. In <strong>HSV</strong>, Hue represents pure wavelength, Saturation represents purity, and Value represents brightness. In <strong>CIE LAB</strong>, $L^*$ represents perceptual lightness, while $a^*$ and $b^*$ represent green-red and blue-yellow opponent color axes.</p>
    `,
    operations: [
      { id: "convert", label: "Convert Colour Spaces", icon: "fa-palette", params: [
        { id: "target_space", label: "Target Colour Space", type: "select", options: [
          { value: "rgb", label: "RGB (Standard Red, Green, Blue)" },
          { value: "gray", label: "Grayscale (Monochrome Luminance)" },
          { value: "hsv", label: "HSV (Hue, Saturation, Value)" },
          { value: "lab", label: "CIE L*a*b* (Perceptual Opponent Space)" },
          { value: "ycrcb", label: "YCrCb (Luma & Chroma Video Standard)" }
        ], default: "hsv" },
        { id: "split_channel", label: "Channel Isolation", type: "select", options: [
          { value: "all", label: "Complete Multi-Channel Representation" },
          { value: "ch1", label: "Channel 1 Only (e.g. Hue / L* / Y)" },
          { value: "ch2", label: "Channel 2 Only (e.g. Saturation / a* / Cr)" },
          { value: "ch3", label: "Channel 3 Only (e.g. Value / b* / Cb)" }
        ], default: "all" }
      ]}
    ]
  }
];

// --- Global Application State ---
const state = {
  activePractical: null,
  activeOperation: null,
  paramValues: {},
  primaryFile: null,
  primaryDataUrl: null,
  primaryDimensions: { width: 0, height: 0 },
  secondaryFile: null,
  secondaryDataUrl: null,
  processedResultUrl: null,
  suggestedFilename: "result.png",
  isProcessing: false,
  viewMode: "side", // "side" or "result"
  // Inpainting Canvas state
  isDrawing: false,
  brushSize: 20,
  hasDrawnMask: false,
  // Camera state
  isFromCamera: false,
  cameraStream: null,
  currentFacingMode: "user"
};

// --- Initialization ---
document.addEventListener("DOMContentLoaded", () => {
  renderHomeCards();
  initDropzones();
  initInpaintingCanvas();
});

// --- Navigation Management ---
function navigateTo(viewName, scrollTarget = null) {
  const homeView = document.getElementById("home-view");
  const workstationView = document.getElementById("workstation-view");
  const navHomeBtn = document.getElementById("nav-home-btn");
  const navPracticalsBtn = document.getElementById("nav-practicals-btn");

  if (viewName === "home") {
    homeView.classList.add("active");
    workstationView.classList.remove("active");
    navHomeBtn.classList.add("active");
    navPracticalsBtn.classList.remove("active");
    window.scrollTo({ top: 0, behavior: "smooth" });

    if (scrollTarget) {
      setTimeout(() => {
        const elem = document.querySelector(scrollTarget);
        if (elem) elem.scrollIntoView({ behavior: "smooth" });
      }, 100);
    }
  } else if (viewName === "workstation") {
    homeView.classList.remove("active");
    workstationView.classList.add("active");
    navHomeBtn.classList.remove("active");
    navPracticalsBtn.classList.add("active");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

// --- Render Home Page Practical Cards ---
function renderHomeCards() {
  const container = document.getElementById("practicals-cards-container");
  if (!container) return;

  container.innerHTML = "";
  PRACTICALS_DATA.forEach(p => {
    const card = document.createElement("div");
    card.className = "practical-card";
    card.setAttribute("data-id", p.id);
    card.setAttribute("data-title", p.title.toLowerCase());

    const opsList = p.operations.map(op => `<span class="card-op-tag">${op.label}</span>`).join("");

    card.innerHTML = `
      <div>
        <div class="card-top">
          <span class="practical-number-badge">${p.number}</span>
          <div class="card-icon"><i class="fa-solid ${p.icon}"></i></div>
        </div>
        <h3 class="card-title">${p.title}</h3>
        <p class="card-desc">${p.desc}</p>
        <div class="card-ops-list">
          ${opsList}
        </div>
      </div>
      <button class="btn-open-practical" onclick="openPractical(${p.id})">
        <i class="fa-solid fa-arrow-right-to-bracket"></i> Open Practical
      </button>
    `;
    container.appendChild(card);
  });
}

// Search Filter
function filterPracticals() {
  const input = document.getElementById("practical-search-input").value.toLowerCase().trim();
  const cards = document.querySelectorAll(".practical-card");
  let count = 0;

  cards.forEach(card => {
    const title = card.getAttribute("data-title");
    const ops = card.querySelector(".card-ops-list").textContent.toLowerCase();
    if (title.includes(input) || ops.includes(input)) {
      card.style.display = "flex";
      count++;
    } else {
      card.style.display = "none";
    }
  });

  const counter = document.getElementById("total-practicals-count");
  if (counter) counter.textContent = count;
}

// --- Launch Practical Workstation ---
function openPractical(practicalId) {
  const practical = PRACTICALS_DATA.find(p => p.id === practicalId);
  if (!practical) return;

  state.activePractical = practical;
  state.activeOperation = practical.operations[0];
  state.paramValues = {};

  // Update Workstation Header
  document.getElementById("workstation-practical-tag").textContent = practical.number;
  document.getElementById("breadcrumb-title").textContent = practical.number;
  document.getElementById("workstation-title").textContent = practical.title;
  document.getElementById("workstation-desc").textContent = practical.desc;
  document.getElementById("theory-content-body").innerHTML = practical.theory;
  document.getElementById("theory-card").classList.remove("open");

  // Render Operation Tabs
  renderOperationTabs(practical);

  // Render Controls for the default operation
  selectOperation(practical.operations[0].id);

  // Clear or prepare preview panels
  clearProcessedResult();

  // If no primary image uploaded, auto-load lab sample image for instant demonstration!
  if (!state.primaryDataUrl) {
    loadSampleImage(false);
  } else {
    updateOrigPreview(state.primaryDataUrl);
  }

  navigateTo("workstation");
}

function toggleTheoryAccordion() {
  const card = document.getElementById("theory-card");
  if (card) card.classList.toggle("open");
}

// --- Operation Tabs Rendering & Selection ---
function renderOperationTabs(practical) {
  const container = document.getElementById("operation-tabs-container");
  container.innerHTML = "";

  practical.operations.forEach((op, index) => {
    const btn = document.createElement("button");
    btn.className = `op-tab-btn ${index === 0 ? "active" : ""}`;
    btn.setAttribute("data-op-id", op.id);
    btn.innerHTML = `<i class="fa-solid ${op.icon || 'fa-gear'}"></i> ${op.label}`;
    btn.onclick = () => selectOperation(op.id);
    container.appendChild(btn);
  });
}

function selectOperation(opId) {
  const op = state.activePractical.operations.find(o => o.id === opId);
  if (!op) return;

  state.activeOperation = op;

  // Update tabs active class
  document.querySelectorAll(".op-tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-op-id") === opId);
  });

  // Toggle secondary dropzone visibility (Practical 1 bitwise AND/OR)
  const secondaryWrap = document.getElementById("secondary-upload-container");
  if (secondaryWrap) {
    secondaryWrap.style.display = op.needsSecondImage ? "block" : "none";
  }

  // Toggle Inpainting Paintbar and Canvas (Practical 6)
  const paintbar = document.getElementById("inpaint-paint-toolbar");
  const inpaintCanvas = document.getElementById("inpaint-drawing-canvas");
  if (state.activePractical.id === 6) {
    paintbar.style.display = "flex";
    inpaintCanvas.style.display = "block";
    resizeInpaintCanvas();
  } else {
    paintbar.style.display = "none";
    inpaintCanvas.style.display = "none";
  }

  // Toggle Practical 7 Compression Metrics Card
  document.getElementById("compression-metrics-card").style.display = (state.activePractical.id === 7) ? "block" : "none";
  // Toggle Practical 9 Detection Metrics Card
  document.getElementById("detection-metrics-card").style.display = (state.activePractical.id === 9) ? "block" : "none";

  // Render parameter controls
  renderParamControls(op);
}

// --- Parameter Controls Renderer ---
function renderParamControls(operation) {
  const container = document.getElementById("params-container");
  container.innerHTML = "";

  if (!operation.params || operation.params.length === 0) {
    container.innerHTML = `<p style="font-size: 0.85rem; color: var(--text-muted);">This operation runs with standard OpenCV defaults and does not require extra parameters.</p>`;
    return;
  }

  operation.params.forEach(param => {
    const val = (state.paramValues[param.id] !== undefined) ? state.paramValues[param.id] : param.default;
    state.paramValues[param.id] = val;

    const group = document.createElement("div");
    group.className = "param-group";

    if (param.type === "slider") {
      group.innerHTML = `
        <div class="param-label-row">
          <label class="param-label" for="param-${param.id}">${param.label}</label>
          <span class="param-value-badge" id="badge-${param.id}">${val}${param.unit || ''}</span>
        </div>
        <input type="range" class="param-slider" id="param-${param.id}" 
               min="${param.min}" max="${param.max}" step="${param.step || 1}" value="${val}"
               oninput="updateSliderParam('${param.id}', this.value, '${param.unit || ''}')" />
      `;
    } else if (param.type === "select") {
      const optionsHtml = param.options.map(opt => `
        <option value="${opt.value}" ${opt.value === val ? 'selected' : ''}>${opt.label}</option>
      `).join("");

      group.innerHTML = `
        <label class="param-label" for="param-${param.id}">${param.label}</label>
        <select class="param-select" id="param-${param.id}" onchange="updateSelectParam('${param.id}', this.value)">
          ${optionsHtml}
        </select>
      `;
    } else if (param.type === "number") {
      group.innerHTML = `
        <label class="param-label" for="param-${param.id}">${param.label}</label>
        <input type="number" class="param-input" id="param-${param.id}" 
               min="${param.min || 0}" value="${val}"
               onchange="updateNumberParam('${param.id}', this.value)" />
      `;
    }

    container.appendChild(group);
  });
}

function updateSliderParam(paramId, value, unit) {
  state.paramValues[paramId] = parseFloat(value);
  const badge = document.getElementById(`badge-${paramId}`);
  if (badge) badge.textContent = `${value}${unit}`;
}

function updateSelectParam(paramId, value) {
  state.paramValues[paramId] = value;
}

function updateNumberParam(paramId, value) {
  state.paramValues[paramId] = parseInt(value, 10);
}

function resetCurrentParams() {
  if (state.activeOperation) {
    state.paramValues = {};
    renderParamControls(state.activeOperation);
    showToast("Parameters reset to default values.", "success");
  }
}

// --- Dropzone & File Handling ---
function initDropzones() {
  const primaryDrop = document.getElementById("primary-dropzone");
  const primaryInput = document.getElementById("primary-file-input");
  const secondaryDrop = document.getElementById("secondary-dropzone");
  const secondaryInput = document.getElementById("secondary-file-input");

  // Primary Dropzone
  primaryDrop.addEventListener("dragover", e => { e.preventDefault(); primaryDrop.classList.add("dragover"); });
  primaryDrop.addEventListener("dragleave", () => primaryDrop.classList.remove("dragover"));
  primaryDrop.addEventListener("drop", e => {
    e.preventDefault();
    primaryDrop.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handlePrimaryFile(e.dataTransfer.files[0]);
    }
  });
  primaryInput.addEventListener("change", e => {
    if (e.target.files && e.target.files.length > 0) {
      handlePrimaryFile(e.target.files[0]);
    }
  });

  // Secondary Dropzone
  secondaryDrop.addEventListener("dragover", e => { e.preventDefault(); secondaryDrop.classList.add("dragover"); });
  secondaryDrop.addEventListener("dragleave", () => secondaryDrop.classList.remove("dragover"));
  secondaryDrop.addEventListener("drop", e => {
    e.preventDefault();
    secondaryDrop.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleSecondaryFile(e.dataTransfer.files[0]);
    }
  });
  secondaryInput.addEventListener("change", e => {
    if (e.target.files && e.target.files.length > 0) {
      handleSecondaryFile(e.target.files[0]);
    }
  });
}

function handlePrimaryFile(file) {
  const allowed = ["image/jpeg", "image/png", "image/webp", "image/jpg"];
  if (!allowed.includes(file.type) && !file.name.match(/\.(jpg|jpeg|png|webp)$/i)) {
    showToast("Invalid file format. Please upload JPG, PNG, or WEBP.", "error");
    return;
  }

  state.primaryFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    state.primaryDataUrl = e.target.result;
    updateOrigPreview(state.primaryDataUrl);
    
    // Update dropzone UI
    document.getElementById("dropzone-prompt").style.display = "none";
    const meta = document.getElementById("primary-file-meta");
    meta.style.display = "flex";
    document.getElementById("primary-filename").textContent = file.name;
    document.getElementById("primary-filesize").textContent = `${(file.size / 1024).toFixed(1)} KB`;

    state.isFromCamera = false;
    const retakeBtn = document.getElementById("btn-retake-camera");
    if (retakeBtn) retakeBtn.style.display = "none";
    const fileIcon = document.getElementById("file-type-icon");
    if (fileIcon) fileIcon.className = "fa-solid fa-file-image";

    // Clear previous drawing
    clearInpaintMask();
    clearProcessedResult();
    showToast(`Loaded ${file.name}`, "success");
  };
  reader.readAsDataURL(file);
}

function handleSecondaryFile(file) {
  state.secondaryFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    state.secondaryDataUrl = e.target.result;
    document.getElementById("secondary-dropzone-prompt").style.display = "none";
    const meta = document.getElementById("secondary-file-meta");
    meta.style.display = "flex";
    document.getElementById("secondary-filename").textContent = file.name;
    showToast(`Loaded second image: ${file.name}`, "success");
  };
  reader.readAsDataURL(file);
}

function clearPrimaryFile(e) {
  if (e) e.stopPropagation();
  state.primaryFile = null;
  state.primaryDataUrl = null;
  state.isFromCamera = false;
  document.getElementById("primary-file-input").value = "";
  document.getElementById("dropzone-prompt").style.display = "block";
  document.getElementById("primary-file-meta").style.display = "none";
  
  const retakeBtn = document.getElementById("btn-retake-camera");
  if (retakeBtn) retakeBtn.style.display = "none";
  
  const origImg = document.getElementById("orig-image-display");
  origImg.style.display = "none";
  origImg.src = "";
  document.getElementById("orig-empty-placeholder").style.display = "block";
  document.getElementById("orig-dim-badge").textContent = "-- x --";
  
  clearInpaintMask();
  clearProcessedResult();
}

function clearSecondaryFile(e) {
  if (e) e.stopPropagation();
  state.secondaryFile = null;
  state.secondaryDataUrl = null;
  document.getElementById("secondary-file-input").value = "";
  document.getElementById("secondary-dropzone-prompt").style.display = "block";
  document.getElementById("secondary-file-meta").style.display = "none";
}

// Load built-in lab sample image
function loadSampleImage(notify = true) {
  const samplePath = (state.activePractical && state.activePractical.sampleImage)
    ? state.activePractical.sampleImage
    : "static/samples/shapes.png";

  fetch(samplePath)
    .then(res => res.blob())
    .then(blob => {
      const filename = samplePath.split("/").pop();
      const file = new File([blob], filename, { type: blob.type || "image/png" });
      handlePrimaryFile(file);
      if (notify) showToast(`Loaded lab sample: ${filename}`, "success");
    })
    .catch(err => {
      console.error("Failed to load sample image:", err);
      showToast("Could not load sample image.", "error");
    });
}

function updateOrigPreview(dataUrl) {
  const origImg = document.getElementById("orig-image-display");
  const placeholder = document.getElementById("orig-empty-placeholder");
  
  origImg.onload = () => {
    state.primaryDimensions = { width: origImg.naturalWidth, height: origImg.naturalHeight };
    document.getElementById("orig-dim-badge").textContent = `${origImg.naturalWidth} x ${origImg.naturalHeight}`;
    resizeInpaintCanvas();
  };
  
  origImg.src = dataUrl;
  origImg.style.display = "block";
  placeholder.style.display = "none";
}

// --- Inpainting Canvas Mask Painter ---
function initInpaintingCanvas() {
  const canvas = document.getElementById("inpaint-drawing-canvas");
  const ctx = canvas.getContext("2d");

  function getCanvasCoords(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.clientX || (e.touches && e.touches[0].clientX);
    const clientY = e.clientY || (e.touches && e.touches[0].clientY);
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY
    };
  }

  function startDraw(e) {
    if (state.activePractical?.id !== 6) return;
    state.isDrawing = true;
    const { x, y } = getCanvasCoords(e);
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.lineWidth = state.brushSize;
    // Semi-transparent red highlight
    ctx.strokeStyle = "rgba(239, 68, 68, 0.85)";
    ctx.lineTo(x, y);
    ctx.stroke();
    state.hasDrawnMask = true;
  }

  function draw(e) {
    if (!state.isDrawing) return;
    e.preventDefault();
    const { x, y } = getCanvasCoords(e);
    ctx.lineTo(x, y);
    ctx.stroke();
    state.hasDrawnMask = true;
  }

  function stopDraw() {
    if (!state.isDrawing) return;
    state.isDrawing = false;
    ctx.closePath();
  }

  canvas.addEventListener("mousedown", startDraw);
  canvas.addEventListener("mousemove", draw);
  window.addEventListener("mouseup", stopDraw);

  canvas.addEventListener("touchstart", startDraw, { passive: false });
  canvas.addEventListener("touchmove", draw, { passive: false });
  window.addEventListener("touchend", stopDraw);
}

function updateBrushSize(val) {
  state.brushSize = parseInt(val, 10);
  document.getElementById("brush-size-val").textContent = val;
}

function clearInpaintMask() {
  const canvas = document.getElementById("inpaint-drawing-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  state.hasDrawnMask = false;
  showToast("Inpaint marking cleared.", "success");
}

function resizeInpaintCanvas() {
  const origImg = document.getElementById("orig-image-display");
  const canvas = document.getElementById("inpaint-drawing-canvas");
  if (!origImg || !canvas || origImg.style.display === "none") return;

  canvas.width = origImg.clientWidth;
  canvas.height = origImg.clientHeight;
  canvas.style.width = `${origImg.clientWidth}px`;
  canvas.style.height = `${origImg.clientHeight}px`;
  canvas.style.top = `${origImg.offsetTop}px`;
  canvas.style.left = `${origImg.offsetLeft}px`;
}

window.addEventListener("resize", () => {
  if (state.activePractical?.id === 6) {
    resizeInpaintCanvas();
  }
});

// Helper: Synthesize sample scratches directly onto canvas
function applySampleScratch() {
  const canvas = document.getElementById("inpaint-drawing-canvas");
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;

  ctx.strokeStyle = "rgba(239, 68, 68, 0.9)";
  ctx.lineWidth = 6;
  ctx.lineCap = "round";

  // Scratch 1
  ctx.beginPath();
  ctx.moveTo(w * 0.15, h * 0.2);
  ctx.lineTo(w * 0.85, h * 0.75);
  ctx.stroke();

  // Scratch 2
  ctx.beginPath();
  ctx.moveTo(w * 0.7, h * 0.15);
  ctx.lineTo(w * 0.3, h * 0.85);
  ctx.stroke();

  state.hasDrawnMask = true;
  showToast("Sample scratches marked on image.", "success");
}

// Generate black-and-white binary mask data URL from canvas
function exportInpaintMaskBase64() {
  const canvas = document.getElementById("inpaint-drawing-canvas");
  if (!canvas || !state.hasDrawnMask) return null;

  // Create an off-screen canvas at image natural resolution
  const offscreen = document.createElement("canvas");
  offscreen.width = state.primaryDimensions.width || canvas.width;
  offscreen.height = state.primaryDimensions.height || canvas.height;
  const offCtx = offscreen.getContext("2d");

  // Fill black
  offCtx.fillStyle = "#000000";
  offCtx.fillRect(0, 0, offscreen.width, offscreen.height);

  // Draw user's brush strokes
  offCtx.drawImage(canvas, 0, 0, offscreen.width, offscreen.height);

  // Convert red/colored strokes to pure white
  const imgData = offCtx.getImageData(0, 0, offscreen.width, offscreen.height);
  const data = imgData.data;
  for (let i = 0; i < data.length; i += 4) {
    // If pixel is not pure black, make it pure white
    if (data[i] > 30 || data[i+1] > 30 || data[i+2] > 30) {
      data[i] = 255;
      data[i+1] = 255;
      data[i+2] = 255;
    } else {
      data[i] = 0;
      data[i+1] = 0;
      data[i+2] = 0;
    }
  }
  offCtx.putImageData(imgData, 0, 0);
  return offscreen.toDataURL("image/png");
}

// --- Process Current Image via Backend API ---
async function processCurrentImage() {
  if (!state.primaryFile && !state.primaryDataUrl) {
    showToast("Please upload an image first or click 'Load Lab Sample'.", "error");
    return;
  }

  if (state.isProcessing) return;
  setProcessingState(true);

  try {
    const formData = new FormData();

    // Primary image
    if (state.primaryFile) {
      formData.append("image", state.primaryFile);
    } else {
      // Convert data URL to blob
      const res = await fetch(state.primaryDataUrl);
      const blob = await res.blob();
      formData.append("image", blob, "image.png");
    }

    formData.append("practical", state.activePractical.id);
    formData.append("operation", state.activeOperation.id);
    formData.append("params", JSON.stringify(state.paramValues));

    // Secondary image if present
    if (state.secondaryFile) {
      formData.append("second_image", state.secondaryFile);
    }

    // Inpainting mask if Practical 6
    let endpoint = "/api/process";
    if (state.activePractical.id === 6) {
      const maskDataUrl = exportInpaintMaskBase64();
      if (!maskDataUrl) {
        showToast("Please draw on the image to mark the damaged area first!", "error");
        setProcessingState(false);
        return;
      }
      formData.append("mask_b64", maskDataUrl);
      endpoint = "/api/inpaint";
    } else if (state.activePractical.id === 7) {
      endpoint = "/api/compress";
    } else if (state.activePractical.id === 9) {
      endpoint = "/api/detect";
    }

    const response = await fetch(endpoint, {
      method: "POST",
      body: formData
    });

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.error || "Image processing failed on server.");
    }

    // Processed Successfully
    displayProcessedResult(result);
    showToast("OpenCV operation completed successfully!", "success");

  } catch (error) {
    console.error("Processing Error:", error);
    showStatusBanner(error.message, true);
    showToast(`Error: ${error.message}`, "error");
  } finally {
    setProcessingState(false);
  }
}

// Display Processed Result in Visualizer
function displayProcessedResult(res) {
  state.processedResultUrl = res.processed_image;
  state.suggestedFilename = res.filename || `practical${state.activePractical.id}_result.png`;

  const procImg = document.getElementById("proc-image-display");
  const placeholder = document.getElementById("proc-empty-placeholder");
  const downloadBtn = document.getElementById("btn-download-result");

  procImg.onload = () => {
    document.getElementById("proc-dim-badge").textContent = `${procImg.naturalWidth} x ${procImg.naturalHeight}`;
  };

  procImg.src = res.processed_image;
  procImg.style.display = "block";
  placeholder.style.display = "none";
  downloadBtn.disabled = false;

  // Status banner
  const runtime = res.execution_time_ms ? `${res.execution_time_ms.toFixed(1)}ms` : "";
  showStatusBanner(res.info?.details || "Operation finished successfully.", false, runtime);

  // Practical 7 Compression Metrics
  if (state.activePractical.id === 7 && res.info) {
    document.getElementById("metric-orig-size").textContent = `${res.info.original_size_kb} KB`;
    document.getElementById("metric-comp-size").textContent = `${res.info.compressed_size_kb} KB`;
    document.getElementById("metric-savings").textContent = `${res.info.savings_percentage}%`;
    document.getElementById("metric-ratio").textContent = `${res.info.compression_ratio}x`;
  }

  // Practical 9 Detection Metrics
  if (state.activePractical.id === 9 && res.info) {
    document.getElementById("metric-detect-count").textContent = res.info.detected_count;
    document.getElementById("metric-cascade-name").textContent = res.info.target_label || "Haar Cascade";
  }
}

function clearProcessedResult() {
  state.processedResultUrl = null;
  const procImg = document.getElementById("proc-image-display");
  procImg.style.display = "none";
  procImg.src = "";
  document.getElementById("proc-empty-placeholder").style.display = "block";
  document.getElementById("proc-dim-badge").textContent = "-- x --";
  document.getElementById("btn-download-result").disabled = true;
  document.getElementById("status-banner").style.display = "none";
}

// --- ONE-CLICK DOWNLOAD HANDLER (VERY IMPORTANT REQUIREMENT) ---
function downloadCurrentResult() {
  if (!state.processedResultUrl) {
    showToast("No processed result available to download.", "error");
    return;
  }

  // Create clean ephemeral anchor to trigger direct browser download
  const link = document.createElement("a");
  link.href = state.processedResultUrl;
  link.download = state.suggestedFilename || `practical_${Date.now()}.png`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  showToast(`Downloaded: ${link.download}`, "success");
}

// Reset Entire Workstation
function resetWorkstation() {
  resetCurrentParams();
  clearInpaintMask();
  clearProcessedResult();
  showToast("Workstation state reset.", "success");
}

// View Mode Toggle (Side-by-side vs Result Only)
function setViewMode(mode) {
  state.viewMode = mode;
  const wrapper = document.getElementById("comparison-wrapper");
  const sideBtn = document.getElementById("btn-mode-side");
  const resBtn = document.getElementById("btn-mode-result");

  if (mode === "side") {
    wrapper.classList.remove("result-only");
    wrapper.classList.add("side-by-side");
    sideBtn.classList.add("active");
    resBtn.classList.remove("active");
  } else {
    wrapper.classList.remove("side-by-side");
    wrapper.classList.add("result-only");
    resBtn.classList.add("active");
    sideBtn.classList.remove("active");
  }
}

// --- UI Feedback & Utilities ---
function setProcessingState(isProcessing) {
  state.isProcessing = isProcessing;
  const spinner = document.getElementById("process-spinner");
  const loader = document.getElementById("processing-loader");
  const btnText = document.getElementById("btn-process-text");
  const btn = document.getElementById("btn-process-image");

  if (isProcessing) {
    spinner.style.display = "inline-block";
    loader.style.display = "flex";
    btnText.textContent = "Processing image...";
    btn.disabled = true;
  } else {
    spinner.style.display = "none";
    loader.style.display = "none";
    btnText.innerHTML = '<i class="fa-solid fa-play"></i> Process Image';
    btn.disabled = false;
  }
}

function showStatusBanner(message, isError = false, runtime = "") {
  const banner = document.getElementById("status-banner");
  const icon = document.getElementById("status-icon");
  const msgElem = document.getElementById("status-message");
  const rtElem = document.getElementById("status-runtime");

  banner.style.display = "flex";
  banner.classList.toggle("error", isError);
  icon.innerHTML = isError ? '<i class="fa-solid fa-circle-exclamation"></i>' : '<i class="fa-solid fa-circle-check"></i>';
  msgElem.textContent = message;
  rtElem.textContent = runtime ? `Execution runtime: ${runtime}` : "";
}

function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <i class="fa-solid ${type === 'success' ? 'fa-circle-check' : 'fa-triangle-exclamation'}"></i>
    <span>${message}</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(20px)";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function openAboutModal() {
  document.getElementById("about-modal").style.display = "flex";
}

function closeAboutModal() {
  document.getElementById("about-modal").style.display = "none";
}

// --- Live Camera Capture (MediaDevices API) ---
async function openCameraModal(e) {
  if (e) e.stopPropagation();
  const modal = document.getElementById("camera-modal");
  modal.style.display = "flex";

  const promptOverlay = document.getElementById("camera-prompt-overlay");
  promptOverlay.style.display = "flex";
  promptOverlay.innerHTML = `
    <div class="loader-spinner"></div>
    <p id="camera-prompt-text">Accessing camera...</p>
    <span id="camera-prompt-sub">Please allow camera permissions if prompted by your browser</span>
  `;

  await startCameraStream();
}

async function startCameraStream() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    const promptOverlay = document.getElementById("camera-prompt-overlay");
    promptOverlay.innerHTML = `
      <i class="fa-solid fa-triangle-exclamation" style="font-size: 2.2rem; color: var(--accent-rose); margin-bottom: 0.6rem;"></i>
      <p style="color: var(--accent-rose); font-weight: 700;">Camera API Unsupported</p>
      <span style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.25rem;">
        Your browser or environment does not support navigator.mediaDevices.getUserMedia().
      </span>
    `;
    showToast("Camera API is not supported in this browser.", "error");
    return;
  }

  try {
    stopCameraStream();

    const constraints = {
      video: {
        facingMode: state.currentFacingMode,
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    };

    state.cameraStream = await navigator.mediaDevices.getUserMedia(constraints);
    const video = document.getElementById("camera-video-stream");
    video.srcObject = state.cameraStream;

    video.onloadedmetadata = () => {
      video.play();
      document.getElementById("camera-prompt-overlay").style.display = "none";
    };

  } catch (err) {
    console.error("Camera access failed:", err);
    let userMsg = "Please allow camera access in your browser settings.";
    if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
      userMsg = "Permission denied. Please grant camera permission in your browser address bar.";
    } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
      userMsg = "No camera hardware detected on this device.";
    } else if (err.name === "NotReadableError" || err.name === "TrackStartError") {
      userMsg = "Camera is currently in use by another application.";
    }

    const promptOverlay = document.getElementById("camera-prompt-overlay");
    promptOverlay.style.display = "flex";
    promptOverlay.innerHTML = `
      <i class="fa-solid fa-video-slash" style="font-size: 2.2rem; color: var(--accent-rose); margin-bottom: 0.6rem;"></i>
      <p style="color: var(--accent-rose); font-weight: 700;">Camera Access Failed</p>
      <span style="font-size: 0.82rem; color: #cbd5e1; margin-top: 0.35rem; max-width: 420px; line-height: 1.4;">
        ${userMsg}
      </span>
      <button class="btn btn-sm btn-secondary" onclick="startCameraStream()" style="margin-top: 1rem;">
        <i class="fa-solid fa-rotate-right"></i> Try Again
      </button>
    `;
    showToast(`Camera Error: ${err.name}`, "error");
  }
}

function stopCameraStream() {
  if (state.cameraStream) {
    state.cameraStream.getTracks().forEach(track => track.stop());
    state.cameraStream = null;
  }
  const video = document.getElementById("camera-video-stream");
  if (video) video.srcObject = null;
}

function closeCameraModal() {
  stopCameraStream();
  const modal = document.getElementById("camera-modal");
  if (modal) modal.style.display = "none";
}

async function switchCamera() {
  state.currentFacingMode = (state.currentFacingMode === "user") ? "environment" : "user";
  const promptOverlay = document.getElementById("camera-prompt-overlay");
  promptOverlay.style.display = "flex";
  promptOverlay.innerHTML = `
    <div class="loader-spinner"></div>
    <p>Switching camera...</p>
  `;
  await startCameraStream();
}

function capturePhotoFromStream() {
  const video = document.getElementById("camera-video-stream");
  const canvas = document.getElementById("camera-capture-canvas");

  if (!video || !video.videoWidth || !video.videoHeight) {
    showToast("Camera stream is not ready yet.", "error");
    return;
  }

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");

  // If user facing mode, flip horizontally for mirror effect if preferred or draw directly
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    if (!blob) {
      showToast("Failed to capture photo frame.", "error");
      return;
    }

    const now = new Date();
    const pad = n => String(n).padStart(2, '0');
    const timeStr = `${now.getHours()}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
    const filename = `camera_photo_${timeStr}.png`;
    const file = new File([blob], filename, { type: "image/png" });

    // Update global state
    state.primaryFile = file;
    state.primaryDataUrl = canvas.toDataURL("image/png");
    state.isFromCamera = true;

    // Update main image preview
    updateOrigPreview(state.primaryDataUrl);

    // Update dropzone UI
    document.getElementById("dropzone-prompt").style.display = "none";
    const meta = document.getElementById("primary-file-meta");
    meta.style.display = "flex";
    document.getElementById("primary-filename").textContent = `${filename} (Camera)`;
    document.getElementById("primary-filesize").textContent = `${(blob.size / 1024).toFixed(1)} KB`;
    
    const fileIcon = document.getElementById("file-type-icon");
    if (fileIcon) fileIcon.className = "fa-solid fa-camera";

    // Show Retake button
    const retakeBtn = document.getElementById("btn-retake-camera");
    if (retakeBtn) retakeBtn.style.display = "inline-flex";

    // Clear previous results & masks
    clearInpaintMask();
    clearProcessedResult();

    // Turn off camera and close modal
    closeCameraModal();

    showToast("Photo captured from Camera! Ready for OpenCV processing.", "success");
  }, "image/png");
}

window.addEventListener("click", e => {
  const aboutModal = document.getElementById("about-modal");
  const cameraModal = document.getElementById("camera-modal");
  if (e.target === aboutModal) closeAboutModal();
  if (e.target === cameraModal) closeCameraModal();
});
