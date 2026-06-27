# 🎓 Education Consultant Chatbot

A simple, friendly AI chatbot that helps students with **college admissions, career planning, scholarships, studying abroad, course selection, and exam prep**. Built with [Gradio](https://www.gradio.app/) and powered by the [Groq](https://groq.com/) LLM API for fast responses.

> Pick a topic, ask your question, and get clear, practical, and encouraging guidance — streamed in real time.

---

## ✨ Features

- 💬 **Streaming replies** — answers appear word-by-word instead of after a long pause
- 🗂️ **Topic selector** — focus the assistant on admissions, careers, scholarships, study abroad, course selection, or exam prep
- 🧠 **Conversation memory** — the bot remembers earlier messages in the chat (bounded to the most recent turns, so long chats stay fast)
- 💡 **Example questions** — one-click starter prompts if you're not sure what to ask
- ⚡ **Fast inference** via Groq
- 🛡️ **Graceful error handling** for missing API keys, timeouts, and network issues

---

## 🛠️ Tech Stack

- **Python**
- **Gradio** — web UI
- **Groq API** — LLM inference (model: `openai/gpt-oss-20b`, overridable)
- **python-dotenv** — loads your API key from a local `.env` file

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/MuhammadBilal-00/Education-Consultant-AI-Bot.git
cd Education-Consultant-AI-Bot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Groq API key

Get a free key from the [Groq Console](https://console.groq.com/keys). Copy
`.env.example` to `.env` and fill it in:

```bash
cp .env.example .env
```

```
GROQ_API_KEY=your_groq_api_key_here
```

`.env` is gitignored, so your key never gets committed.

### 5. Run the app

```bash
python app.py
```

Open the local URL shown in your terminal (usually `http://127.0.0.1:7860`).

---

## ☁️ Deploy on Hugging Face Spaces

1. Create a new **Gradio** Space.
2. Upload `app.py` and `requirements.txt`.
3. Go to **Settings → Variables and secrets** and add a **secret** named `GROQ_API_KEY` with your key (no `.env` file needed — Spaces injects it directly).
4. The Space builds automatically — that's it!

---

## 📦 Requirements

`requirements.txt`:

```
gradio==5.29.0
requests>=2.31
python-dotenv>=1.0
```

---

## 🤖 A Note on the Model

This project uses `openai/gpt-oss-20b` by default. Groq periodically retires older models — if you ever see an error like `model_decommissioned`, check the [Groq deprecations page](https://console.groq.com/docs/deprecations) and either:

- set `GROQ_MODEL=<new-model-name>` in your `.env` (no code changes needed), or
- update the `MODEL_NAME` default in `app.py`.

---

## 📁 Project Structure

```
.
├── app.py             # Main application
├── requirements.txt   # Dependencies
├── .env.example        # Template for your local API key — copy to .env
├── .gitignore
└── README.md          # You are here
```

---

## 📄 License

Released under the MIT License. Feel free to use, modify, and share.

---

## 🙌 Acknowledgements

- [Gradio](https://www.gradio.app/) for the UI framework
- [Groq](https://groq.com/) for fast LLM inference

---

*Built by [Muhammad Bilal](https://github.com/MuhammadBilal-00).*
