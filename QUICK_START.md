# 🚀 MindCare Multimodal - QUICK START GUIDE

## ⚡ 5-Minute Quick Start

### What You Have
A mental health chatbot with **real-time multimodal emotion detection**:
- 💬 Text emotion detection
- 🎤 Audio emotion detection  
- 📹 Video emotion detection
- 🧠 AI-powered empathetic responses

---

## 📦 Installation (5 minutes)

### Step 1: Open Terminal in Project Root
```bash
cd "c:\final project\mental-health-project"
```

### Step 2: Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 3: Create .env File
Create `backend/.env` with:
```
DATABASE_URL=sqlite:///./mindcare.db
SECRET_KEY=your-secret-key-minimum-32-characters-very-long-phrase
GROQ_API_KEY=your-groq-api-key-from-console.groq.com
ADB_PATH=adb
MODEL_PATH=./models/trained_ravdess_model.h5
```

### Step 4: Frontend Setup (New Terminal)
```bash
cd frontend/client
npm install
```

---

## 🎯 Running the App

### Terminal 1: Start Backend
```bash
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload --port 8000
```
✅ Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2: Start Frontend
```bash
cd frontend/client
npm run dev
```
✅ Wait for: `Local: http://localhost:5173/`

### Open Browser
Go to: **http://localhost:5173**

---

## 🎮 How to Use

### 1️⃣ Register & Login
- Click "Sign Up"
- Create account
- Login

### 2️⃣ Text Mode
- Type message
- Click "Send"
- See emotion detection below response

### 3️⃣ Audio Mode
- Click 🎤 "Record Audio"
- Speak for 5 seconds
- Click "⏹ Stop Audio"
- Click "Send"
- See audio analysis

### 4️⃣ Video Mode
- Click 📹 "Record Video"
- Face camera for 5 seconds
- Click "⏹ Stop Video"
- Click "Send"
- See facial emotion analysis

### 5️⃣ Multimodal (Best!)
- Type message
- Click 🎤 Record Audio
- Click 📹 Record Video
- Click "Send"
- See fused emotion from all 3!

---

## 📊 What You'll See

Each bot message shows:
```
"I understand you're feeling frustrated..."

😊 Emotion: frustrated (87.3%)
[multimodal]
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Change to 8001: `--port 8001` |
| Microphone access denied | Check browser permissions (🔒 icon) |
| Camera access denied | Allow access when prompted |
| Slow response (5+ sec) | Normal! Models loading. Try again. |
| CORS error | Backend CORS already configured ✅ |
| npm not found | Install Node.js from nodejs.org |
| Python not found | Install Python from python.org |

---

## 🧠 Emotion Detection Explained

### Text
Uses AI to understand emotion from words
- "I'm sad" → Emotion: sad
- "That's awesome!" → Emotion: happy

### Audio
Analyzes voice characteristics
- Angry tone → High energy, fast speech
- Sad tone → Low energy, slow speech
- Happy tone → Varied pitch, energetic

### Video
Detects facial micro-expressions
- Happy: Smile, raised cheeks
- Sad: Frown, lowered eyes
- Angry: Furrowed brows, tight lips

### Fusion
Combines all 3 for best result:
- Text 40% + Audio 35% + Video 25%
- If algorithms disagree, weighted vote wins

---

## 📁 Project Structure

```
backend/
  ├── agents/emotion_detection_agents/
  │   ├── text_analysis.py   ← Text emotion
  │   ├── audio_emt.py       ← Audio emotion (NEW)
  │   ├── video_emt.py       ← Video emotion (NEW)
  │   └── fusion.py          ← Fusion engine (UPDATED)
  ├── services/
  │   └── chat_service.py    ← Orchestrates all (UPDATED)
  └── routers/
      └── chat.py            ← API endpoint (UPDATED)

frontend/
  └── client/src/
      ├── pages/Chat.jsx               ← Main page (UPDATED)
      └── components/ChatInput.jsx     ← Recording (NEW)
```

---

## 🔐 Get GROQ API Key (1 minute)

1. Go to: https://console.groq.com
2. Sign up (free)
3. Click "API Keys"
4. Create new key
5. Copy and paste in `.env` as `GROQ_API_KEY`

---

## ✨ Features Breakdown

| Feature | Tech | Status |
|---------|------|--------|
| Text emotion | Transformers | ✅ |
| Audio emotion | Librosa + spectral analysis | ✅ |
| Video emotion | DeepFace | ✅ |
| Emotion fusion | Weighted algorithm | ✅ |
| Chat responses | Groq LLM | ✅ |
| Risk detection | Groq LLM | ✅ |
| Parallel processing | Asyncio | ✅ |
| Web UI | React + Tailwind | ✅ |

---

## 🎬 Demo Flow

```
User: 👤 [Types] "I'm so nervous about my exam"
         [Records voice with anxious tone]
         [Records face showing worry]

App: 🧠 Detects:
     - Text emotion: fearful (78%)
     - Audio emotion: fearful (82%)
     - Video emotion: fearful (75%)
     → Fused: fearful (78.3%)

Bot: 💬 "I can hear the worry in your voice. 
         It's completely normal to feel nervous before an exam..."
     + Shows: 😊 Emotion: fearful (78.3%) [multimodal]
```

---

## ⚠️ Important Notes

1. **First Load is Slow**: Models load on first use (~30 sec) - be patient!
2. **Recording Quality**: Clear audio and good lighting work best
3. **Permissions**: Allow camera/microphone when prompted
4. **Browser**: Chrome/Firefox work best
5. **Data**: Not stored on server (localStorage only, cleared on logout)

---

## 🚀 Next Steps

After running:
1. Create an account
2. Test each mode (text, audio, video)
3. Try multimodal together
4. Check browser console (F12) for logs
5. Check backend terminal for processing details

---

## 📞 Common Questions

**Q: Can I modify emotions detected?**
A: No, they're auto-detected. But you can adjust weights in `fusion.py`

**Q: Why is audio processing slow?**
A: Feature extraction takes time. Models run on CPU by default.

**Q: Can I use this on mobile?**
A: Not yet - needs desktop for proper audio/video recording

**Q: Is my data secure?**
A: Not production-ready. Use HTTPS + better auth for deployment

**Q: Can I change the LLM model?**
A: Yes! Edit `agents/chat_agent.py` - change model name in Groq call

---

## 🎓 Learning Resources

- **Emotion Detection**: See `docs/COMPONENTS.md`
- **Architecture**: See `docs/ARCHITECTURE.md`
- **Full Setup**: See `MULTIMODAL_SETUP.md`
- **All Changes**: See `CHANGES.md`

---

## ✅ Verification: Everything Works If:

- ✅ Backend starts successfully
- ✅ Frontend loads without errors
- ✅ Can login/signup
- ✅ Text message shows emotion
- ✅ Audio recording works
- ✅ Video recording works
- ✅ Multimodal shows emotion from all 3
- ✅ No red errors in browser console

---

## 🎉 You're Ready!

Your multimodal mental health chatbot is live and working!

**Enjoy helping users understand their emotions through AI-powered analysis.** 🧠💙

---

## 📊 System Requirements Met?

- Python 3.10+ ✅
- Node.js 18+ ✅
- 8GB RAM (works, 16GB better) ✅
- Webcam + Microphone (optional) ✅
- 5GB disk space ✅

You're all set! 🚀
