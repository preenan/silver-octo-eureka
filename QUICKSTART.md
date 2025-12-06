# 🚀 Quick Start - Render Deployment

## Files to Upload to GitHub

Upload these files from your `server/` folder:

1. ✅ `main.py` - Main server file (updated for Render)
2. ✅ `requirements.txt` - Python dependencies
3. ✅ `Procfile` - Tells Render how to start the app
4. ✅ `.gitignore` - Ignore unnecessary files
5. ✅ `README.md` - Documentation

**Also copy from `babu taka strealmit app/` folder:**
6. ✅ `best_currency_model (1).h5` - Your trained model
7. ✅ `labels.txt` - Currency labels

---

## Render Configuration (Copy-Paste Ready)

When creating Web Service on Render:

| Field | Value |
|-------|-------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Instance Type | Free |

---

## After Deployment

1. Get your URL: `https://your-app.onrender.com`
2. Test: Open in browser - should show API status
3. Update Flutter app:

**Edit `lib/services/api_service.dart` line 7:**
```dart
static const String baseUrl = 'https://your-app.onrender.com';
```

4. Run app: `flutter run`

---

## ⚠️ Important

- First request after inactivity takes ~30 seconds (free tier sleeps)
- If memory errors occur, upgrade to Starter ($7/month)
- Model files MUST be in same directory as main.py on GitHub

---

**Full guide**: See `RENDER_DEPLOYMENT.md`
