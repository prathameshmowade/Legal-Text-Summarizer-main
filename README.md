# LexAI – Legal Document Summarizer

Developed by **Ayush D. Badwaik**, **Prathamesh Mowade**, **Sudhanshu Sathwane**, **Sriyansh Sheel**

---

## Project Structure

```
lexai/
├── app.py               ← Flask backend (set your API key here)
├── requirements.txt     ← Python dependencies
├── render.yaml          ← Render deployment config
└── templates/
    └── index.html       ← Frontend (served by Flask)
```

---

## 1. Set Your API Key

Open `app.py` and replace:
```python
GROK_API_KEY = "your_api_key_here"
```
with your actual Grok API key from [x.ai](https://x.ai).

---

## 2. Run Locally

```bash
pip install -r requirements.txt
python app.py
```
Open → http://localhost:5000

---

## 3. Deploy on Render

1. Push this folder to a **GitHub repository**
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Deploy**
5. Your app will be live at `https://lexai.onrender.com` (or similar)

> ⚠️ **Never commit your real API key to GitHub.**  
> Instead, set it as an **Environment Variable** on Render:  
> Dashboard → Your Service → Environment → Add `GROK_API_KEY = your_key`  
> Then update `app.py` to use:
> ```python
> GROK_API_KEY = os.environ.get("GROK_API_KEY", "")
> ```

---

## Features

- 🏛 Professional light-theme UI with smooth animations
- 🔊 Sound effect on Summarize button click
- 📄 Paste text or upload `.txt` files
- ⚖ 7-section structured legal analysis via Grok-3
- 📋 Copy output to clipboard
- 📊 Stats: word count, sections, time, risk level
- 🚀 Render-ready with `gunicorn`
