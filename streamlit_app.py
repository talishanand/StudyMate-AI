import os
import random
from datetime import datetime

import streamlit as st
from google import genai

# ---------- page config ----------
st.set_page_config(page_title="StudyMate AI", page_icon="⚡", layout="centered")

MODEL = "gemini-2.5-flash"

SUBJECTS = ["General", "Math", "Physics", "CS", "Biology"]

DEPTH_MODES = {
    "Quick": "Answer in 2-4 concise sentences. No filler, straight to the point.",
    "Balanced": "Give a clear, well-structured explanation of moderate length.",
    "Deep dive": "Give a thorough, in-depth explanation with examples and step-by-step reasoning.",
}

STARTER_PROMPTS = [
    "Explain recursion like I'm new to it",
    "What's the difference between TCP and UDP?",
    "Give me a worked example of Bayes' theorem",
    "Why does photosynthesis need light?",
]

THINKING_LINES = [
    "Charging up",
    "Sparking a synapse",
    "Conducting the answer",
    "Channeling some volts",
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


def build_query(prompt: str, subject: str, depth: str) -> str:
    parts = [DEPTH_MODES[depth]]
    if subject != "General":
        parts.append(f"The topic is {subject}.")
    parts.append(f"Question: {prompt}")
    return "\n".join(parts)


# ---------- styling: electric purple / black ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg: #060107;
        --surface: #150a1e;
        --surface-raised: #1e0f2c;
        --border: #4c2a80;
        --text: #f5ecff;
        --text-dim: #a793d1;
        --purple: #9d00ff;
        --purple-bright: #d896ff;
        --pink: #ff3ec8;
        --glow: rgba(157, 0, 255, 0.65);
    }

    .stApp {
        background:
            radial-gradient(circle at 20% 10%, rgba(157,0,255,0.20) 0, transparent 40%),
            radial-gradient(circle at 85% 80%, rgba(255,62,200,0.14) 0, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(157,0,255,0.06) 0, transparent 60%),
            var(--bg);
        color: var(--text);
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 760px; }

    /* ---------- hero ---------- */
    .hero-row { display: flex; align-items: center; gap: 10px; }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        background: linear-gradient(90deg, var(--purple-bright), var(--pink));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .bolt {
        font-size: 1.8rem;
        animation: flicker 3.2s infinite;
        filter: drop-shadow(0 0 10px var(--glow)) drop-shadow(0 0 20px var(--glow));
    }
    @keyframes flicker {
        0%, 91%, 100% { opacity: 1; }
        92% { opacity: 0.2; }
        93% { opacity: 1; }
        94% { opacity: 0.3; }
        95% { opacity: 1; }
    }
    .hero-tagline {
        color: var(--text-dim);
        font-size: 1rem;
        margin-top: 8px;
        margin-bottom: 22px;
    }

    /* ---------- generic button base ---------- */
    div[data-testid="stButton"] button {
        border-radius: 10px;
        transition: box-shadow 150ms, border-color 150ms, transform 100ms;
    }
    div[data-testid="stButton"] button:hover {
        box-shadow: 0 0 20px var(--glow), 0 0 40px var(--glow);
        transform: translateY(-1px);
    }

    /* ---------- starter prompt cards ---------- */
    div[class*="st-key-starters"] div[data-testid="stButton"] button {
        background: var(--surface) !important;
        border: 1px dashed var(--border) !important;
        color: var(--text-dim) !important;
        font-size: 0.82rem !important;
        padding: 10px 12px !important;
        height: auto !important;
        white-space: normal !important;
        text-align: left !important;
    }
    div[class*="st-key-starters"] div[data-testid="stButton"] button:hover {
        border-color: var(--purple) !important;
        color: var(--purple-bright) !important;
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
        border: 1px solid var(--border) !important;
        color: var(--text-dim) !important;
    }
    div[class*="st-key-subjects"] div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(90deg, var(--purple), var(--pink)) !important;
        border: 1px solid var(--purple) !important;
        color: #060107 !important;
        font-weight: 700 !important;
        box-shadow: 0 0 22px var(--glow), 0 0 44px var(--glow);
    }

    /* ---------- depth segmented control ---------- */
    div[class*="st-key-depth"] div[data-testid="stButton"] button {
        font-size: 0.78rem !important;
        padding: 4px 14px !important;
        height: auto !important;
        border-radius: 8px !important;
    }
    div[class*="st-key-depth"] div[data-testid="stButton"] button[kind="secondary"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-dim) !important;
    }
    div[class*="st-key-depth"] div[data-testid="stButton"] button[kind="primary"] {
        background: var(--surface-raised) !important;
        border: 1px solid var(--purple) !important;
        color: var(--purple-bright) !important;
    }

    /* ---------- chat bubbles ---------- */
    .bubble-row { display: flex; margin: 14px 0; }
    .bubble-row.user { justify-content: flex-end; }
    .bubble-row.assistant { justify-content: flex-start; flex-direction: column; }

    .bubble {
        max-width: 88%;
        padding: 12px 16px;
        border-radius: 12px;
        line-height: 1.6;
        animation: rise 350ms ease-out;
    }
    @keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

    .bubble.user {
        background: var(--surface-raised);
        border: 1px solid var(--border);
        font-size: 0.94rem;
        color: var(--text);
    }

    /* recolor st.code blocks (used for assistant answers -> gives a free copy button) */
    div[data-testid="stCodeBlock"] pre {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-left: 3px solid var(--purple) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 20px rgba(168,85,247,0.08);
    }
    div[data-testid="stCodeBlock"] code {
        color: var(--text) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
    }

    /* ---------- chat input ---------- */
    div[data-testid="stChatInput"] textarea {
        background: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        box-shadow: 0 0 0 1px var(--purple), 0 0 18px var(--glow);
        border-radius: 12px;
    }
    div[data-testid="stChatInput"] {
        border-top: 1px solid var(--border);
        padding-top: 12px;
    }

    /* ---------- sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(90deg, var(--purple-bright), var(--pink));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    div[data-testid="stMetric"] {
        background: var(--surface-raised);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 10px 12px;
    }
    div[data-testid="stMetricValue"] { color: var(--purple-bright) !important; }

    /* ---------- empty state ---------- */
    .empty-board {
        text-align: center;
        color: var(--text-dim);
        padding: 30px 0 10px;
    }
    .empty-board .big {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        color: var(--purple-bright);
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
if "depth" not in st.session_state:
    st.session_state.depth = "Balanced"
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "started_at" not in st.session_state:
    st.session_state.started_at = datetime.now()


def render_answer(text: str):
    st.code(text, language=None)


def notes_markdown() -> str:
    lines = [f"# StudyMate notes — {st.session_state.started_at:%Y-%m-%d %H:%M}", ""]
    for m in st.session_state.messages:
        if m["role"] == "user":
            lines.append(f"## Q: {m['content']}")
        else:
            lines.append(m["content"])
            lines.append("")
    return "\n".join(lines)


# ---------- sidebar ----------
with st.sidebar:
    st.markdown("### ⚡ StudyMate")
    st.caption("An AI study assistant powered by Gemini.")
    st.divider()

    asked_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
    st.metric("Questions asked", asked_count)

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
    if st.session_state.messages:
        st.download_button(
            "⬇️ Download notes (.md)",
            data=notes_markdown(),
            file_name="studymate_notes.md",
            mime="text/markdown",
            use_container_width=True,
        )
    if st.button("🧹 Clear board", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------- hero ----------
st.markdown(
    '<div class="hero-row"><span class="bolt">⚡</span><span class="hero-title">StudyMate</span></div>',
    unsafe_allow_html=True,
)
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

# ---------- depth control ----------
with st.container(key="depth"):
    cols = st.columns(len(DEPTH_MODES))
    for col, mode in zip(cols, DEPTH_MODES):
        with col:
            is_active = st.session_state.depth == mode
            btn_type = "primary" if is_active else "secondary"
            if st.button(mode, key=f"depth_{mode}", type=btn_type, use_container_width=True):
                st.session_state.depth = mode
                st.rerun()

# ---------- starter prompts (only before the first question) ----------
if not st.session_state.messages:
    st.markdown(
        '<div class="empty-board"><div class="big">fully charged. ask away.</div>'
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
    if msg["role"] == "user":
        st.markdown(
            f'<div class="bubble-row user"><div class="bubble user">{msg["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="bubble-row assistant">', unsafe_allow_html=True)
        render_answer(msg["content"])
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- regenerate last answer ----------
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    if st.button("🔁 Regenerate last answer"):
        last_user_msg = next(
            (m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"),
            None,
        )
        if last_user_msg:
            query = build_query(last_user_msg, st.session_state.subject, st.session_state.depth)
            with st.spinner(random.choice(THINKING_LINES) + "…"):
                try:
                    answer = ask_gemini(query)
                except Exception:
                    answer = "Sorry, I couldn't answer that. Please try again."
            st.session_state.messages[-1] = {"role": "assistant", "content": answer}
            st.rerun()

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

    query = build_query(prompt, st.session_state.subject, st.session_state.depth)

    with st.spinner(random.choice(THINKING_LINES) + "…"):
        try:
            answer = ask_gemini(query)
        except Exception:
            answer = "Sorry, I couldn't answer that. Please try again."

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
