# MindCare Multimodal Setup Guide

## 📋 Overview

This guide explains how to set up and run the MindCare Mental Health application with **full multimodal support** (Text, Audio, and Video emotion detection running in parallel).

### ✨ New Multimodal Features

- **Text Analysis**: Emotion detection using transformer-based sentiment analysis
- **Audio Analysis**: Emotion detection using spectral features (MFCC, energy, zero-crossing rate)
- **Video Analysis**: Facial emotion detection using DeepFace
- **Fusion Engine**: Smart weighted combination of all modalities for better accuracy
- **Parallel Processing**: All inputs processed simultaneously
- **Real-time Detection**: Instant emotion feedback displayed in chat

---

## 🔧 Prerequisites

### System Requirements
- **Windows/Mac/Linux**: Any OS with Python 3.10+ and Node.js 18+
- **RAM**: Minimum 8GB (16GB recommended for faster processing)
- **Storage**: 5GB free space (for dependencies)
- **Webcam/Microphone**: For audio/video features (optional)

### Software Requirements
| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.10+ | Backend runtime |
| Node.js | 18+ | Frontend runtime |
| npm | 9+ | Package manager |

---

## 📦 Step 1: Installation

### 1.1 Clone the Repository

```bash
cd "c:\final project"
git clone <your-repo-url>
cd mental-health-project
```

### 1.2 Backend Setup

#### Create Virtual Environment

```bash
cd backend
python -m venv venv
```

#### Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This includes:
- FastAPI & Uvicorn (Web server)
- SQLAlchemy (Database ORM)
- Transformers (Text emotion detection)
- Librosa (Audio processing)
- OpenCV & DeepFace (Video emotion detection)
- TensorFlow (Deep learning)

### 1.3 Frontend Setup

```bash
cd ../frontend/client
npm install
```

---

## ⚙️ Step 2: Configuration

### 2.1 Create Backend Environment File

In the `backend/` directory, create `.env`:

```bash
cd backend
cp .env.example .env  # or create new file
```

Edit `.env` with your values:

```env
# Database
DATABASE_URL=sqlite:///./mindcare.db

# Security - Generate a random secret key
SECRET_KEY=your-super-secret-key-here-minimum-32-characters

# API Keys
GROQ_API_KEY=your-groq-api-key-from-console.groq.com

# Android Debug Bridge
ADB_PATH=C:/path/to/adb.exe  # Or just "adb" if in PATH

# Model Path
MODEL_PATH=./models/trained_ravdess_model.h5
```

### 2.2 Get API Keys

#### Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new key
5. Copy and paste in `.env`

---

## 🚀 Step 3: Running the Application

### 3.1 Start Backend Server

```bash
cd backend
# Make sure virtual environment is activated
python -m uvicorn main:app --reload --port 8000
```

✅ You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

Keep this terminal running.

### 3.2 Start Frontend Development Server

In a **new terminal**:

```bash
cd frontend/client
npm run dev
```

✅ You should see:
```
  VITE v7.2.4  ready in XXms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### 3.3 Open Application

Open your browser and go to: **http://localhost:5173**

---

## 💬 Step 4: Using Multimodal Features

### Text-Only Mode
1. Type a message in the input field
2. Click "Send"
3. Emotion detected from text
4. Response includes emotion analysis

### Audio-Only Mode
1. Click **"🎤 Record Audio"** button
2. Speak your message
3. Click **"⏹ Stop Audio"** when done
4. Click "Send"
5. Audio emotion detected separately
6. Response uses audio emotion context

### Video-Only Mode
1. Click **"📹 Record Video"** button
2. Face the camera and speak
3. Click **"⏹ Stop Video"** when done
4. Click "Send"
5. Facial emotion detected
6. Response uses video emotion analysis

### Multimodal (Text + Audio + Video)
1. **Type text** in input field
2. **Click "🎤 Record Audio"** to record voice
3. **Click "📹 Record Video"** to record video
4. Click "Send"
5. All three modalities analyzed in **parallel**
6. Emotions **fused** together using weighted algorithm
7. Response uses combined emotion analysis

✨ **The system will show**:
- Detected single emotion at header
- Confidence score (0-100%)
- Detection mode used [text-only/audio-only/video-only/multimodal]

---

## 🧠 Emotion Detection Details

### Text Analysis
Uses `j-hartmann/emotion-english-distilroberta-base` model
- **Maps to**: angry, disgust, fearful, happy, neutral, sad, surprised

### Audio Analysis  
Analyzes spectral features:
- **MFCC** (Mel-frequency cepstral coefficients)
- **Energy** (amplitude/intensity)
- **ZCR** (Zero-crossing rate)
- **Spectral Centroid** (frequency characteristics)

Detected emotions:
- Happy: Medium-high energy + high spectral centroid
- Sad: Low energy + low ZCR
- Angry: High energy + high ZCR
- Calm: Low key + low energy
- Fearful: High arousal + negative features
- Neutral: Default

### Video Analysis
Uses DeepFace library for facial recognition
- Analyzes facial micro-expressions
- Returns 8 emotion classes
- Maps: anger, disgust, fear, happiness, neutral, sadness, surprise

### Emotion Fusion
**Weighted Combination**:
- Text: 40% weight (most reliable)
- Audio: 35% weight (vocal cues)
- Video: 25% weight (facial expressions)

Formula:
```
Fused Score = (Text_conf × 0.4) + (Audio_conf × 0.35) + (Video_conf × 0.25)
```

---

## 🔐 Troubleshooting

### Port Already in Use
```bash
# Change port (replace 8001 with any available port)
python -m uvicorn main:app --reload --port 8001
```

Then update frontend API call in `src/pages/Chat.jsx`:
```javascript
await fetch("http://localhost:8001/api/chat/message", ...)
```

### Microphone/Camera Permission Denied
- Check browser permissions (top-left address bar)
- Allow access when prompted
- Try in incognito mode
- Check OS-level privacy settings

### Audio/Video Not Recording
1. Refresh browser
2. Check browser console (F12) for errors
3. Verify camera/microphone working (try other app)
4. Clear browser cache

### Slow Processing
- Audio/video processing can take 2-5 seconds
- Normal for first request (model loading)
- Subsequent requests faster

### CORS Errors
If you see CORS errors, ensure backend CORS config includes:
```python
allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"]
```

---

## 📊 Project Structure

```
mental-health-project/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Configuration
│   ├── database.py              # Database setup
│   ├── models.py                # User model
│   ├── schemas.py               # Request/response schemas (UPDATED)
│   ├── auth.py                  # JWT authentication
│   ├── agents/
│   │   ├── chat_agent.py        # LLM responses
│   │   ├── alert_agent.py       # Risk detection
│   │   └── emotion_detection_agents/
│   │       ├── text_analysis.py       # Text emotion (ENHANCED)
│   │       ├── audio_emt.py           # Audio emotion (NEW)
│   │       ├── video_emt.py           # Video emotion (NEW)
│   │       └── fusion.py              # Emotion fusion (ENHANCED)
│   ├── services/
│   │   ├── chat_service.py      # Chat logic (ENHANCED WITH MULTIMODAL)
│   │   └── alert_service.py     # Emergency alerts
│   └── routers/
│       ├── auth.py              # Authentication endpoints
│       ├── chat.py              # Chat endpoints (UPDATED)
│       └── emotion.py           # Emotion endpoints
│
├── frontend/
│   └── client/
│       ├── src/
│       │   ├── pages/
│       │   │   ├── Chat.jsx     # Main chat (UPDATED WITH MULTIMODAL)
│       │   │   ├── Login.jsx
│       │   │   ├── SignUp.jsx
│       │   │   └── Crisis.jsx
│       │   ├── components/
│       │   │   ├── ChatInput.jsx      # Input control (UPDATED WITH RECORDING)
│       │   │   ├── MessageBubble.jsx  # Messages (UPDATED WITH EMOTION DISPLAY)
│       │   │   ├── ChatHeader.jsx
│       │   │   ├── Sidebar.jsx
│       │   │   ├── CameraView.jsx
│       │   │   └── RiskAlertBanner.jsx
│       │   ├── api/
│       │   │   ├── auth.js
│       │   │   └── chatApi.js
│       │   ├── context/
│       │   │   └── MediaDevicesContext.jsx
│       │   ├── hooks/
│       │   │   └── useMediaDevices.js
│       │   └── utils/
│       │       ├── storage.js
│       │       └── riskDetection.js
│       └── package.json
│
└── docs/
    ├── ARCHITECTURE.md
    ├── COMPONENTS.md
    └── MULTIMODAL_SETUP.md (THIS FILE)
```

---

## 🧪 Testing Multimodal Features

### Test 1: Text-Only Detection
```
Input: "I'm feeling sad today"
Expected: Emotion = "sad", Mode = "text-only"
```

### Test 2: Audio-Only Detection
```
Input: Record cheerful voice
Expected: Emotion = "happy", Mode = "audio-only"
```

### Test 3: Video-Only Detection
```
Input: Record happy facial expression
Expected: Emotion = "happy", Mode = "video-only"
```

### Test 4: Multimodal Fusion
```
Input: Sad text + Happy voice + Happy face
Expected: Emotion depends on fusion weights (should lean toward happy)
Mode = "multimodal"
```

---

## 📈 Performance Tips

1. **First Load**: Models load on first use (~30 seconds)
2. **Subsequent Requests**: 2-3 seconds per message
3. **GPU Acceleration**: Install `tensorflow-gpu` for faster processing (optional)
4. **Batch Processing**: The system processes all modalities in parallel

---

## 🔒 Security Notes

- Tokens stored in localStorage (not production-grade)
- Use HTTPS in production
- Never commit `.env` file with real keys
- Validate all inputs on server-side

---

## 📚 Additional Resources

- **FastAPI Docs**: http://localhost:8000/docs
- **Transformers Library**: https://huggingface.co/transformers/
- **Librosa Documentation**: https://librosa.org/
- **DeepFace GitHub**: https://github.com/serengp/deepface

---

## ✅ Verification Checklist

Before considering setup complete, verify:

- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:5173
- [ ] Can create account and login
- [ ] Text messages work and show emotion
- [ ] Microphone recording works
- [ ] Camera recording works
- [ ] Multimodal messages process correctly
- [ ] Emotion detection displays in message bubbles
- [ ] No CORS or permission errors in browser console

---

## 🎉 You're All Set!

Your MindCare Mental Health application with **full multimodal emotion detection** is now running. Users can:

✅ Chat with text
✅ Record and send audio messages
✅ Record and send video messages
✅ Combine any modalities together
✅ Get real-time emotion feedback
✅ Receive empathetic AI responses based on detected emotions

Enjoy! 🚀
