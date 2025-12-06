import os
import io
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from typing import Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Currency Recognition API", version="1.0.0")

# Add CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration - Updated for Render deployment
# For local testing, use relative path to parent folder
# For Render, model files should be in the same directory
if os.path.exists(os.path.join(os.path.dirname(__file__), "best_currency_model (1).h5")):
    # Render deployment (model in same directory)
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "best_currency_model (1).h5")
    LABELS_PATH = os.path.join(os.path.dirname(__file__), "labels.txt")
else:
    # Local development (model in parent folder)
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "babu taka strealmit app", "best_currency_model (1).h5")
    LABELS_PATH = os.path.join(os.path.dirname(__file__), "..", "babu taka strealmit app", "labels.txt")

IMG_SIZE = (224, 224)

# Global variables
model = None
class_labels = []

# Exchange rates to BDT (Bangladeshi Taka)
EXCHANGE_RATES = {
    'usd': 120.0,      # 1 USD = 120 BDT
    'taka': 1.0,       # 1 BDT = 1 BDT
    'rupee': 1.4,      # 1 INR = 1.4 BDT
    'baht': 3.5,       # 1 THB = 3.5 BDT
}

# Currency names in Bengali
CURRENCY_NAMES = {
    'usd': 'আমেরিকান ডলার',
    'taka': 'বাংলাদেশী টাকা',
    'rupee': 'ভারতীয় রুপি',
    'baht': 'থাই বাথ',
}


def load_model():
    """Load the .h5 model"""
    global model
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        logger.info(f"Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise


def load_labels():
    """Load class labels from file"""
    global class_labels
    try:
        if os.path.exists(LABELS_PATH):
            with open(LABELS_PATH, 'r', encoding='utf-8') as f:
                class_labels = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(class_labels)} labels")
        else:
            logger.warning("Labels file not found, using default class names")
            class_labels = [f"class_{i}" for i in range(27)]
    except Exception as e:
        logger.error(f"Error loading labels: {e}")
        class_labels = [f"class_{i}" for i in range(27)]


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Preprocess image for model inference"""
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB and resize
        image = image.convert('RGB').resize(IMG_SIZE)
        
        # Convert to numpy array and normalize
        img_array = np.array(image, dtype=np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise HTTPException(status_code=400, detail="Invalid image format")


def parse_label(label: str) -> Dict:
    """Parse label to extract amount and currency"""
    try:
        parts = label.split('_')
        if len(parts) < 2:
            return None
        
        amount = int(parts[0])
        currency_code = parts[1].lower()
        
        # Get currency name and exchange rate
        currency_name = CURRENCY_NAMES.get(currency_code, currency_code.capitalize())
        exchange_rate = EXCHANGE_RATES.get(currency_code, 1.0)
        
        # Calculate BDT equivalent
        bdt_amount = int(amount * exchange_rate)
        
        return {
            'amount': amount,
            'currency_code': currency_code,
            'currency_name': currency_name,
            'exchange_rate': exchange_rate,
            'bdt_equivalent': bdt_amount
        }
    except Exception as e:
        logger.error(f"Error parsing label {label}: {e}")
        return None


def to_bangla_number(num: int) -> str:
    """Convert English numbers to Bangla"""
    bangla_digits = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', 
                     '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'}
    return ''.join(bangla_digits.get(d, d) for d in str(num))


@app.on_event("startup")
async def startup_event():
    """Load model and labels on startup"""
    load_model()
    load_labels()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Currency Recognition API is running",
        "status": "ok",
        "model_loaded": model is not None,
        "labels_loaded": len(class_labels) > 0,
        "total_classes": len(class_labels)
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict currency from uploaded image
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Preprocess image
        processed_image = preprocess_image(image_bytes)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get top prediction
        predicted_idx = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))
        
        # Get label
        if predicted_idx < len(class_labels):
            label = class_labels[predicted_idx]
        else:
            label = f"class_{predicted_idx}"
        
        # Parse label
        parsed = parse_label(label)
        
        # Generate description in Bengali
        description = ""
        if parsed:
            amount_bangla = to_bangla_number(parsed['amount'])
            if parsed['currency_code'] == 'taka':
                description = f"{amount_bangla} {parsed['currency_name']}"
            else:
                bdt_bangla = to_bangla_number(parsed['bdt_equivalent'])
                description = f"{amount_bangla} {parsed['currency_name']} প্রায় {bdt_bangla} টাকার সমান"
        else:
            description = label
        
        # Get top 5 predictions
        top_5_indices = np.argsort(predictions[0])[::-1][:5]
        top_5 = [
            {
                'label': class_labels[i] if i < len(class_labels) else f"class_{i}",
                'confidence': float(predictions[0][i])
            }
            for i in top_5_indices
        ]
        
        # Return result
        return {
            'success': True,
            'label': label,
            'confidence': confidence,
            'description': description,
            'details': parsed,
            'top_5': top_5
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
