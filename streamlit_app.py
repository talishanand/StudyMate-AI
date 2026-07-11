import os
import random

import streamlit as st
from google import genai

# ---------- page config ----------
st.set_page_config(page_title="StudyMate AI", page_icon="📘", layout="centered")

MODEL = "gemini-2.5-flash"

STARTER_PROMPTS = [
    "Explain recursion like I'm new to it",
    "What's the difference between TCP and UDP?",
    "Give me a worked example of Bayes' theorem",
    "Why does photosynthesis need light?",
]

THINKING_LINES = [
    "Chalking it out",
    "Working through the steps",
    "Flipping to the right page",
    "Sketching out an answer",
]


# ---------- api key + client ----------
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.environ.get("GEMINI_API_KEY")


API_KEY = get_api_key()

if not API_KEY:
    st.error(
        "GEMINI_API_KEY is not set.\n\n"
        "- **Local dev:** create `.streamlit/secrets.toml` with `GEMINI_API_KEY = \"your-key\"`, "
        "or set it as an environment variable.\n"
        "- **Streamlit Cloud:** add it under your app's Settings → Secrets."
    )
    st.stop()


@st.cache_resource
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


client = get_client(API_KEY)


def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text


# ---------- styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --board: #182420;
        --board-raised: #22322c;
        --board-line: #3a4d47;
        --chalk: #efe8d8;
        --chalk-dim: #a9b6ae;
        --sage: #7fa88f;
        --yellow: #eab54c;
        --coral: #e2725b;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(239,232,216,0.03) 0, transparent 35%),
            radial-gradient(circle at 85% 75%, rgba(239,232,216,0.025) 0, transparent 40%),
            var(--board);
        color: var(--chalk);
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* kill default streamlit chrome we don't want */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 760px; }

    /* ---------- hero ---------- */
    .hero-title {
        font-family: 'Kalam', cursive;
        font-size: 2.6rem;
        color: var(--yellow);
        margin-bottom: 0;
        position: relative;
        width: fit-content;
    }
    .hero-title::after {
        content: "";
        position: absolute;
        left: 2px;
        bottom: -4px;
        height: 4px;
        width: 0%;
        background: var(--yellow);
        border-radius: 2px;
        animation: draw 900ms ease-out 200ms forwards;
    }
    @keyframes draw { to { width: calc(100% - 4px); } }

    .hero-tagline {
        color: var(--chalk-dim);
        font-size: 1rem;
        margin-top: 10px;
        margin-bottom: 24px;
    }

    /* ---------- starter prompt "sticky notes" ---------- */
    div[class*="st-key-starters"] div[data-testid="stButton"] button {
        background: var(--board-raised) !important;
        border: 1px dashed var(--board-line) !important;
        color: var(--chalk-dim) !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        padding: 10px 12px !important;
        height: auto !important;
        white-space: normal !important;
        text-align: left !important;
        transition: transform 120ms, border-color 120ms, color 120ms;
    }
    div[class*="st-key-starters"] div[data-testid="stButton"] button:hover {
        border-color: var(--yellow) !important;
        color: var(--yellow) !important;
        transform: translateY(-2px);
    }

    /* ---------- subject chips ---------- */
    div[class*="st-key-subjects"] div[data-testid="stButton"] button {
        border-radius: 999px !important;
        font-size: 0.8rem !important;
        padding: 4px 16px !important;
        height: auto !important;
    }
    div[class*="st-key-subjects"] div[data-testid="stButton"] button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid var(--board-line) !important;
        color: var(--chalk-dim) !important;
    }
    div[class*="st-key-subjects"] div[data-testid="stButton"] button[kind="primary"] {
        background: var(--yellow) !important;
        border: 1px solid var(--yellow) !important;
        color: #24201a !important;
        font-weight: 600 !important;
    }

    /* ---------- chat bubbles (custom, not default st.chat_message) ---------- */
    .bubble-row { display: flex; margin: 14px 0; }
    .bubble-row.user { justify-content: flex-end; }
    .bubble-row.assistant { justify-content: flex-start; }

    .bubble {
        max-width: 88%;
        padding: 12px 16px;
        border-radius: 12px;
        line-height: 1.6;
        animation: rise 350ms ease-out;
    }
    @keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

    .bubble.user {
        background: var(--board-raised);
        border: 1px solid var(--board-line);
        font-size: 0.94rem;
        color: var(--chalk);
    }

    .bubble.assistant {
        background: transparent;
        border-left: 2px solid var(--yellow);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.86rem;
        color: var(--chalk);
        white-space: pre-wrap;
        padding-left: 16px;
    }

    /* ---------- chat input ---------- */
    div[data-testid="stChatInput"] textarea {
        background: var(--board-raised) !important;
        color: var(--chalk) !important;
        border: 1px solid var(--board-line) !important;
    }
    div[data-testid="stChatInput"] {
        border-top: 2px dashed var(--board-line);
        padding-top: 12px;
    }

    /* ---------- sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: var(--board-raised);
        border-right: 2px dashed var(--board-line);
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'Kalam', cursive;
        color: var(--yellow);
    }

    /* ---------- empty state ---------- */
    .empty-board {
        text-align: center;
        color: var(--board-line);
        padding: 40px 0 20px;
    }
    .empty-board .big {
        font-family: 'Kalam', cursive;
        font-size: 1.3rem;
        color: var(--sage);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "subject" not in st.session_state:
    st.session_state.subject = "General"
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

SUBJECTS = ["General", "Math", "Physics", "CS", "Biology"]

# ---------- sidebar ----------
with st.sidebar:
    st.markdown("### 📘 StudyMate")
    st.caption("An AI study assistant powered by Gemini.")
    st.divider()

    st.markdown("**Recent questions**")
    user_qs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
    if not user_qs:
        st.caption("_Nothing asked yet._")
    else:
        for q in reversed(user_qs[-10:]):
            label = q[:40] + ("…" if len(q) > 40 else "")
            if st.button(label, key=f"hist_{hash(q)}", use_container_width=True):
                st.session_state.pending_prompt = q

    st.divider()
    if st.button("🧹 Clear board", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------- hero ----------
st.markdown('<div class="hero-title">StudyMate</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-tagline">Ask a question about anything you\'re studying. Get it explained clearly.</div>',
    unsafe_allow_html=True,
)

# ---------- subject chips ----------
with st.container(key="subjects"):
    cols = st.columns(len(SUBJECTS))
    for col, subj in zip(cols, SUBJECTS):
        with col:
            is_active = st.session_state.subject == subj
            btn_type = "primary" if is_active else "secondary"
            if st.button(subj, key=f"subj_{subj}", type=btn_type, use_container_width=True):
                st.session_state.subject = subj
                st.rerun()

# ---------- starter prompts (only before the first question) ----------
if not st.session_state.messages:
    st.markdown(
        '<div class="empty-board"><div class="big">the board is clean.</div>'
        "Try one of these, or write your own below.</div>",
        unsafe_allow_html=True,
    )
    with st.container(key="starters"):
        cols = st.columns(2)
        for i, sp in enumerate(STARTER_PROMPTS):
            with cols[i % 2]:
                if st.button(sp, key=f"starter_{i}", use_container_width=True):
                    st.session_state.pending_prompt = sp

# ---------- render conversation ----------
for msg in st.session_state.messages:
    role = msg["role"]
    st.markdown(
        f'<div class="bubble-row {role}"><div class="bubble {role}">{msg["content"]}</div></div>',
        unsafe_allow_html=True,
    )

# ---------- input ----------
typed_prompt = st.chat_input("e.g. Explain how binary search works")
prompt = st.session_state.pending_prompt or typed_prompt
st.session_state.pending_prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f'<div class="bubble-row user"><div class="bubble user">{prompt}</div></div>',
        unsafe_allow_html=True,
    )

    query = (
        prompt
        if st.session_state.subject == "General"
        else f"[Subject: {st.session_state.subject}] {prompt}"
    )

    with st.spinner(random.choice(THINKING_LINES) + "…"):
        try:
            answer = ask_gemini(query)
        except Exception:
            answer = "Sorry, I couldn't answer that. Please try again."

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
