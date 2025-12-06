# Currency Recognition Server

FastAPI server for currency classification using TensorFlow model.

## Setup

1. **Install Python dependencies:**
```bash
cd server
pip install -r requirements.txt
```

2. **Run the server:**
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### GET `/`
Health check endpoint. Returns server status and model info.

**Response:**
```json
{
  "message": "Currency Recognition API is running",
  "status": "ok",
  "model_loaded": true,
  "labels_loaded": true,
  "total_classes": 27
}
```

### POST `/predict`
Predict currency from uploaded image.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (image file)

**Response:**
```json
{
  "success": true,
  "label": "100_usd",
  "confidence": 0.95,
  "description": "১০০ আমেরিকান ডলার প্রায় ১২০০০ টাকার সমান",
  "details": {
    "amount": 100,
    "currency_code": "usd",
    "currency_name": "আমেরিকান ডলার",
    "exchange_rate": 120.0,
    "bdt_equivalent": 12000
  },
  "top_5": [...]
}
```

## Testing with curl

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@/path/to/currency_image.jpg"
```

## Configuration

The server automatically loads:
- Model: `../babu taka strealmit app/best_currency_model (1).h5`
- Labels: `../babu taka strealmit app/labels.txt`

## Supported Currencies

- 🇺🇸 USD (American Dollar)
- 🇧🇩 Taka (Bangladeshi Taka)
- 🇮🇳 Rupee (Indian Rupee)
- 🇹🇭 Baht (Thai Baht)

Total: 27 currency classes
