import os

import streamlit as st
from google import genai

# ---------- config ----------
st.set_page_config(page_title="StudyMate AI", page_icon="📘", layout="centered")

MODEL = "gemini-2.5-flash"


def get_api_key() -> str | None:
    """Prefer Streamlit secrets (used on Streamlit Cloud); fall back to a local env var."""
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


# ---------- styling (chalkboard theme) ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1e2b28;
        color: #ede6d3;
    }
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        color: #e8b94a !important;
    }
    .stChatMessage {
        background-color: #263a35 !important;
        border-radius: 10px;
    }
    .stChatMessage p, .stChatMessage div {
        color: #ede6d3 !important;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: #263a35 !important;
        color: #ede6d3 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- sidebar ----------
with st.sidebar:
    st.markdown("### 📘 StudyMate AI")
    st.caption("An AI study assistant powered by Gemini.")

    subject = st.selectbox(
        "Subject (optional)",
        ["General", "Math", "Physics", "CS", "Biology"],
    )

    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------- chat state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("StudyMate AI")
st.caption("Ask a question about anything you're studying — get a clear explanation back.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- input ----------
prompt = st.chat_input("e.g. Explain how binary search works")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    query = prompt if subject == "General" else f"[Subject: {subject}] {prompt}"

    with st.chat_message("assistant"):
        with st.spinner("Working it out..."):
            try:
                answer = ask_gemini(query)
            except Exception:
                answer = "Sorry, I couldn't answer that. Please try again."
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
