# 🚀 Deploy to Render.com - Complete Guide

## Prerequisites
- GitHub account
- Render.com account (free)
- Your server code ready

---

## Step 1: Prepare Your Repository

### 1.1 Create a GitHub Repository

1. Go to https://github.com and create a new repository
2. Name it: `currency-recognition-server`
3. Make it **Public** (required for Render free tier)
4. Don't initialize with README

### 1.2 Upload Server Files

**Option A: Using GitHub Web Interface**

1. Go to your new repository
2. Click "uploading an existing file"
3. Drag and drop these files from `server/` folder:
   - `main.py`
   - `requirements.txt`
   - `Procfile`
   - `README.md`
   - `.gitignore`
4. **IMPORTANT**: Also upload from `babu taka strealmit app/`:
   - `best_currency_model (1).h5`
   - `labels.txt`
5. Commit the files

**Option B: Using Git Command Line**

```bash
cd "c:\Users\NAZRUL ISLAM\Downloads\baburtaka\babur_taka\server"

# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial server setup"

# Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/currency-recognition-server.git

# Push
git branch -M main
git push -u origin main
```

---

## Step 2: Update main.py for Render

The paths in `main.py` need to be updated because the model will be in the same directory on Render.

**Change lines 26-27 in `server/main.py`:**

```python
# OLD (for local):
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "babu taka strealmit app", "best_currency_model (1).h5")
LABELS_PATH = os.path.join(os.path.dirname(__file__), "..", "babu taka strealmit app", "labels.txt")

# NEW (for Render):
MODEL_PATH = os.path.join(os.path.dirname(__file__), "best_currency_model (1).h5")
LABELS_PATH = os.path.join(os.path.dirname(__file__), "labels.txt")
```

---

## Step 3: Deploy on Render

### 3.1 Sign Up for Render
1. Go to https://render.com
2. Sign up with your GitHub account

### 3.2 Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `currency-recognition-server`
3. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `currency-recognition-api` (or your choice) |
| **Region** | Choose closest to Bangladesh (Singapore recommended) |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

4. **Instance Type**: Select **Free**
5. Click **"Create Web Service"**

### 3.3 Wait for Deployment

- First deployment takes ~5-10 minutes
- You'll see build logs
- Wait for status to show "Live" with a green dot

---

## Step 4: Get Your API URL

After deployment succeeds:

1. You'll see a URL like: `https://currency-recognition-api.onrender.com`
2. Copy this URL
3. Test it in browser: `https://currency-recognition-api.onrender.com/`
4. You should see:
   ```json
   {
     "message": "Currency Recognition API is running",
     "status": "ok"
   }
   ```

---

## Step 5: Update Flutter App

### 5.1 Update API URL

Edit `lib/services/api_service.dart`:

```dart
class ApiService {
  // Replace with your Render URL
  static const String baseUrl = 'https://currency-recognition-api.onrender.com';
  
  // rest of the code...
}
```

### 5.2 Test the App

```bash
flutter run
```

---

## 🎯 Your Render URL Structure

```
https://currency-recognition-api.onrender.com/          # Health check
https://currency-recognition-api.onrender.com/predict   # Image upload
```

---

## ⚠️ Important Notes

### Free Tier Limitations:
- ✅ **750 hours/month free** (enough for testing)
- ⚠️ **Sleeps after 15 mins of inactivity** (first request takes ~30 seconds to wake up)
- ✅ **Automatic HTTPS**
- ⚠️ **Limited to 512MB RAM** (may be tight for TensorFlow)

### If You Get Memory Errors:
The TensorFlow model might exceed free tier memory. If deployment fails with memory errors:

**Option 1**: Upgrade to Starter plan ($7/month) with 512MB+ RAM

**Option 2**: Use smaller model or optimize:
```python
# Add to main.py after imports
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')  # Disable GPU usage
```

---

## 🔧 Troubleshooting

### Build Failed?
- Check `requirements.txt` is correct
- Verify Python version compatibility
- Check Render build logs for errors

### App Running but Predictions Fail?
- Verify model and labels files are uploaded
- Check file paths in `main.py`
- View Render logs for errors

### Cold Start Too Slow?
- Free tier sleeps after inactivity
- Consider paid tier ($7/month) for always-on
- Or use Render's "Background Worker" to keep warm

---

## 📊 Monitor Your App

1. Go to Render Dashboard
2. Click on your service
3. View:
   - **Logs** - See server output
   - **Metrics** - CPU/Memory usage
   - **Events** - Deployment history

---

## 🎉 You're Done!

Your API is now live at:
```
https://your-app-name.onrender.com
```

Update your Flutter app with this URL and test! 🚀

---

## Next Steps

1. ✅ Deploy to Render
2. ✅ Update Flutter app with Render URL
3. ✅ Test with real currency images
4. ✅ Share the app with kids to enjoy!

**Need help?** Check Render documentation: https://render.com/docs
