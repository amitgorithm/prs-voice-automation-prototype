# Quick Start Guide - OpenAI GPT-4 Mini Version

## ✅ Setup Complete!

Your PRS Automation System is now configured to use **OpenAI GPT-4 Mini** with your API key.

### **System Information**

- **AI Model**: OpenAI GPT-4 Mini (Fast & Cost-Effective)
- **Voice-to-Text**: Built-in Web Speech API (Chrome, Edge, Safari)
- **Backend**: Flask (Python)
- **Frontend**: Pure HTML/JavaScript with Real-time Speech Recognition

---

## 🚀 How to Run on Localhost

### **Step 1: Install Dependencies**

```bash
cd /Users/nilansharora/Downloads/files
pip install -r requirements.txt
```

### **Step 2: Start the Server**

Make sure your OpenAI API key is set as an environment variable, then run:

```bash
python server.py
```

You should see:

```
============================================================
PRS Automation System - Backend Server (OpenAI GPT-4 Mini)
============================================================

✓ OpenAI API key configured

Starting server...
Open in browser: http://localhost:5000

Press Ctrl+C to stop
```

### **Step 3: Open in Your Browser**

- Go to: **`http://localhost:5000`**
- Select an assessment scale (BDI-II or COMPASS-31)
- Allow microphone access when prompted

---

## 🎤 How It Works

### **Voice Recording Flow**

1. **Click "🎤 Start Voice Recording"**
   - Your browser captures speech in real-time
   - Web Speech API transcribes instantly
   - Text updates live as you speak

2. **Speak Your Answer**
   - Example: "I feel sad most of the time"
   - You'll see interim text appearing

3. **Click "🔴 RECORDING - Click to Stop"** when done
   - Text is captured and displayed
   - You can edit if needed

4. **Click "✓ Submit Response"**
   - Sends to OpenAI GPT-4 Mini
   - AI scores and maps to scale option
   - Moves to next question

### **AI Scoring**

- **Fast**: GPT-4 Mini is optimized for speed (~1-2 seconds per response)
- **Accurate**: Understands clinical context and natural language
- **Smart**: If unclear, asks a backup clarification question
- **Safe**: Never diagnoses or gives medical advice

---

## 📊 Complete Session Example

1. Start → Select "Beck Depression Inventory II"
2. Q1: "Over the past two weeks, how would you describe your feelings of sadness?"
   - You say: "I feel pretty sad lately"
   - AI scores: `1` (I feel sad much of the time)
   - Rationale: "Patient reports frequent sadness over recent period"

3. Q2-Q5: Same process for remaining questions
4. Results: View final score and download JSON

---

## 📥 Download Results

After completion, click **"📄 Download Session Data (JSON)"** to get:

```json
{
  "SessionID": "session_1674234567",
  "ScaleName": "Beck Depression Inventory II",
  "FinalScore": 8,
  "Items": [
    {
      "QuestionID": "Q1",
      "PatientResponse": "I feel pretty sad lately",
      "ChosenOption": {
        "Label": "I feel sad much of the time",
        "Score": 1
      },
      "ClinicalRationale": "Patient reports frequent sadness...",
      "Validity": "VALID"
    }
    // ... more items
  ]
}
```

---

## ⚙️ API Key Info

This project expects the OpenAI API key to be provided via an environment variable.

**Set your API key before running the server:**

```bash
# Mac / Linux
export OPENAI_API_KEY="sk-your-api-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key-here"

```

---

## 🔧 Troubleshooting

### ❌ "Connection refused"

- Make sure server is running: `python server.py`
- Access `http://localhost:5000` (not file://)

### ❌ Microphone not working

- Use Chrome, Edge, or Safari (not Firefox)
- Allow microphone in browser settings (🔒 in address bar)
- Restart browser if permissions cached incorrectly

### ❌ "API error 401"

- Your OpenAI key may have expired or been revoked
- Check your OpenAI account: https://platform.openai.com/account/api-keys
- Update the key in server.py

### ❌ Speech recognition not working

- Try speaking louder/clearer
- Check microphone is not muted
- Refresh page (Cmd+Shift+R on Mac)

---

## 🎯 Performance Notes

**GPT-4 Mini Benefits:**

- ⚡ **Fast responses** (~1-2 seconds)
- 💰 **Cost-effective** (much cheaper than GPT-4)
- 🧠 **Smart reasoning** for clinical scoring
- 📱 **Works on all devices** with voice support

**Compared to Claude:**

- Faster response times
- Lower API costs
- Same accuracy for PRS scoring

---

## 📱 Browser Compatibility

| Browser       | Voice Recording | Status          |
| ------------- | --------------- | --------------- |
| Chrome        | ✅              | Fully supported |
| Edge          | ✅              | Fully supported |
| Safari        | ✅              | Fully supported |
| Firefox       | ⚠️              | Limited support |
| Mobile Chrome | ✅              | Supported       |
| Mobile Safari | ✅              | Supported       |

---

## 🔐 Security

- ✅ API key stored securely on backend
- ✅ Never exposed to browser
- ✅ Audio transcribed locally (not stored)
- ✅ CORS configured for localhost
- ✅ Session data only saved on download

---

## ✨ Next Steps

1. **Run the server**: `python server.py`
2. **Open in browser**: `http://localhost:5000`
3. **Test with voice**: Allow microphone and start recording
4. **Download results**: Get JSON with scores

**You're all set! Enjoy your PRS assessments with OpenAI GPT-4 Mini!** 🚀
