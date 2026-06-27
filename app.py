import gradio as gr
import os
import json
import requests
from dotenv import load_dotenv

# Loads variables from a local .env file (no-op if the file doesn't exist,
# e.g. on Hugging Face Spaces where secrets are injected directly).
load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# llama3-8b-8192 was decommissioned. Its replacement (llama-3.1-8b-instant)
# was itself deprecated on 2026-06-17, so we use the current recommended model.
# Override via GROQ_MODEL in .env if Groq deprecates this one too.
MODEL_NAME = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")

# Number of prior chat messages (user+assistant) sent to the API as context.
# Keeps the request payload bounded on long conversations.
MAX_HISTORY_MESSAGES = 20

SYSTEM_PROMPT = (
    "You are a knowledgeable and supportive education consultant. "
    "You help students with college admissions, career planning, scholarship "
    "advice, and studying abroad. Your answers are clear, practical, and "
    "encouraging."
)


# ── Groq call (streaming) ───────────────────────────────────────────────────
def stream_groq(api_messages):
    """Yield reply text chunk-by-chunk from the Groq API."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": api_messages,
        "temperature": 0.7,
        "max_tokens": 2048,
        "stream": True,
    }

    try:
        with requests.post(
            GROQ_API_URL, headers=headers, json=payload, stream=True, timeout=60
        ) as r:
            if r.status_code != 200:
                yield f"⚠️ Error {r.status_code}: {r.text}"
                return

            for line in r.iter_lines():
                if not line:
                    continue
                line = line.decode("utf-8")
                if not line.startswith("data: "):
                    continue
                data = line[6:]
                if data.strip() == "[DONE]":
                    break
                try:
                    delta = json.loads(data)["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
    except requests.exceptions.Timeout:
        yield "⚠️ The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        yield f"⚠️ Network error: {e}"


# ── Chat handler ────────────────────────────────────────────────────────────
def respond(message, topic, history):
    message = (message or "").strip()
    if not message:
        yield "", history
        return

    if not GROQ_API_KEY:
        history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content":
                "⚠️ GROQ_API_KEY is not set. Create a `.env` file in the project "
                "folder with `GROQ_API_KEY=your_key_here` (see `.env.example`), "
                "or set it under **Settings → Variables and secrets** if running "
                "on a Hugging Face Space."},
        ]
        yield "", history
        return

    # Messages sent to the model: system prompt + recent turns + topic-tagged turn.
    # Gradio's chatbot history dicts can carry extra fields (e.g. "metadata")
    # that the Groq API rejects, so only role/content are forwarded.
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(
        {"role": m["role"], "content": m["content"]}
        for m in history[-MAX_HISTORY_MESSAGES:]
    )
    api_messages.append({"role": "user", "content": f"[Topic: {topic}] {message}"})

    # Visible chat stores the clean message (no topic tag) + an empty reply to fill
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": ""},
    ]
    yield "", history

    partial = ""
    for chunk in stream_groq(api_messages):
        partial += chunk
        history[-1]["content"] = partial
        yield "", history


# ── UI ──────────────────────────────────────────────────────────────────────
with gr.Blocks(title="Education Consultant Chatbot", theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🎓 Education Consultant Chatbot\nPowered by Groq LLM")

    chatbot = gr.Chatbot(type="messages", height=480, label="Chat")

    with gr.Row():
        topic = gr.Dropdown(
            choices=[
                "College Admissions",
                "Career Guidance",
                "Scholarships & Financial Aid",
                "Study Abroad",
                "Course Selection",
                "Exam Preparation",
            ],
            value="College Admissions",
            label="Select a Topic",
            scale=1,
        )
        msg = gr.Textbox(
            label="Ask your question",
            placeholder="e.g. How do I write a strong personal statement?",
            scale=3,
        )

    with gr.Row():
        send = gr.Button("Send", variant="primary")
        clear = gr.Button("Clear Chat")

    gr.Examples(
        examples=[
            "How do I write a strong personal statement?",
            "What scholarships are available for international students?",
            "How do I choose between a BS and a BA degree?",
            "What's the best way to prepare for the SAT/ACT?",
        ],
        inputs=msg,
        label="Need ideas? Try one of these",
    )

    # Submit on Enter or via the Send button
    msg.submit(respond, [msg, topic, chatbot], [msg, chatbot])
    send.click(respond, [msg, topic, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot)


if __name__ == "__main__":
    demo.launch()