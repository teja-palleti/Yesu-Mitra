# Yesu Mitra - Biblical Chatbot (Ready to Use!)

## 🎉 Your Complete Chatbot Package

This package contains **everything** you need to run your Telugu Biblical Chatbot!

### ✅ What's Included:

- ✅ **Pre-configured Groq API** - Your API key is already embedded
- ✅ **Web interface** - Beautiful chat UI
- ✅ **Telugu Text-to-Speech** - Audio playback
- ✅ **All features working** - RAG, semantic search, contextual notes
- ✅ **100% FREE** - No costs, no credit cards

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

Open PowerShell or Command Prompt in this folder and run:

```bash
pip install openai gtts flask
```

### Step 2: Download Telugu Bible Data

Run the download script:

```bash
python download_telugu_bible.py
```

This will automatically download the complete Telugu Bible (11.2 MB) from GitHub.

**Alternative:** If the script doesn't work, download manually:
1. Visit: https://github.com/godlytalias/Bible-Database
2. Download `Telugu/bible.json`
3. Save it as `telugu_bible.json` in this folder

### Step 3: Start the Chatbot

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

That's it! 🎉

---

## 📁 Files in This Package

```
yesu_mitra_chatbot/
│
├── app.py                          # Flask web server
├── chatbot_backend.py             # Core chatbot logic (with Groq API)
├── download_telugu_bible.py       # Bible data downloader
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
└── templates/
    └── index.html                  # Web interface
```

---

## 🔑 Your Groq API Key

Your API key is already embedded in `chatbot_backend.py`:
```
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
```

**Keep this secure!** Don't share this package publicly with your API key in it.

---

## ✨ Features

1. **Retrieval-Augmented Generation (RAG)** - Answers backed by real Bible verses
2. **Semantic Search** - Understands synonyms and context
3. **Telugu Text-to-Speech** - Listen to verses in Telugu
4. **Simple Language Mode** - Ask for "simple language" for easy explanations
5. **Historical Context** - Ask for "historical context" for background info
6. **Jesus-Believer Persona** - Warm, compassionate responses

---

## 🎯 Example Queries

Try these questions:

- "What does the Bible say about love?"
- "I am worried about my future. What guidance does the Bible offer?"
- "Tell me about the historical context of the Book of Ruth"
- "What verses help with anxiety? Use simple language."
- "దేవుని ప్రేమ గురించి చెప్పండి" (Tell me about God's love in Telugu)

---

## 🔧 Troubleshooting

### "Module 'openai' not found"
```bash
pip install openai gtts flask
```

### "Bible data file not found"
Run: `python download_telugu_bible.py`

### "Can't connect to Groq"
Check your internet connection. The API key is already configured.

### "Port 5000 already in use"
Change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001)  # Use 5001 instead
```

---

## 💡 Technical Details

### AI Model
- **Provider:** Groq (100% FREE)
- **Model:** Llama 3.3 70B Versatile
- **Speed:** 300+ tokens/second
- **Intelligence:** 77.3% MMLU score

### Rate Limits (Free Tier)
- 30 requests per minute
- 1,000 requests per day
- 12,000 tokens per minute

Perfect for personal use!

---

## 🌐 Deploying Online

Want to deploy this chatbot to a website?

### Recommended Platforms:
1. **Render** - https://render.com (Free tier available)
2. **Heroku** - https://heroku.com (Free tier available)
3. **Railway** - https://railway.app (Free $5/month credit)

### Deployment Steps:
1. Create account on chosen platform
2. Connect your GitHub repository (or upload files)
3. Set environment variable: `GROQ_API_KEY=your-key`
4. Deploy!

---

## 📖 Bible Data Source

The Telugu Bible data is sourced from:
- **GitHub Repository:** https://github.com/godlytalias/Bible-Database
- **Format:** JSON
- **Size:** 11.2 MB
- **License:** Open Source

---

## 🙏 Support

If you need help:

1. Check this README
2. Check the error messages carefully
3. Make sure all dependencies are installed
4. Verify `telugu_bible.json` exists

---

## ✝️ May God Bless You!

Your Yesu Mitra chatbot is ready to help you explore the Bible!

**Features:**
- ✅ Fast AI responses (Groq)
- ✅ Complete Telugu Bible
- ✅ Audio playback (TTS)
- ✅ Semantic search
- ✅ 100% FREE forever

**Created with ❤️ and faith**

---

## 📝 License

This chatbot is for personal, educational, and non-commercial use.

The Bible data is open source and freely available.
The Groq API is free for personal projects.

---

## 🔒 Security Note

**IMPORTANT:** Your API key is embedded in `chatbot_backend.py`. 

If you plan to share this code or deploy it publicly:
1. Remove the hardcoded API key
2. Use environment variables instead
3. Add a `.gitignore` file to exclude sensitive data

To use environment variables:
```bash
set GROQ_API_KEY=your-key-here  # Windows
export GROQ_API_KEY=your-key-here  # Linux/Mac
```

---

**Enjoy your Biblical Chatbot! 🙏**
