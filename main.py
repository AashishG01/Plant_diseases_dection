from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import cv2
import tensorflow as tf
from pathlib import Path
import logging

# ----------------------------
# App initialization
# ----------------------------
app = FastAPI(title="Plant Disease Classifier")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Static + Templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Load trained model
MODEL_PATH = BASE_DIR / "models" / "my_model.h5"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    logger.info(f"✅ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    raise RuntimeError(f"Model loading failed: {e}")

# Class labels (ensure consistent with training order)
CATEGORIES = ['Early_blight', 'Late_blight', 'healthy']


# ----------------------------
# Utils
# ----------------------------
def preprocess_image_bytes(image_bytes: bytes, img_size: int = 128):
    """Preprocess uploaded image (bytes → model ready tensor)."""
    try:
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image file")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_size, img_size))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        raise HTTPException(status_code=400, detail=f"Image preprocessing failed: {str(e)}")


# ----------------------------
# Routes
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    """Serve frontend homepage."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Predict plant disease from uploaded leaf image."""
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    contents = await file.read()
    img = preprocess_image_bytes(contents, img_size=128)

    try:
        preds = model.predict(img)
        pred_class = CATEGORIES[int(np.argmax(preds))]
        confidence = float(np.max(preds))
        logger.info(f"Prediction: {pred_class} ({confidence:.2f})")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    return JSONResponse({
    "prediction": pred_class,   # 👈 frontend ke hisaab se
    "confidence": round(confidence, 4)
})
