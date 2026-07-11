# StudyMate AI

An AI-powered study assistant. Ask a question about anything you're studying — a concept, a definition, a worked example — and get a clear, structured explanation back, in your browser.

Started life as a single Colab notebook calling the Gemini API. This repo turns that into a real (small) full-stack app: a Flask backend that talks to Gemini, and a static frontend you can open in any browser.

## Stack

- **Backend:** Python, Flask, `google-genai` (Gemini API)
- **Frontend:** HTML, CSS, vanilla JS (no build step)
- **Model:** `gemini-2.5-flash`

## Project structure

```
study-assistant/
├── backend/
│   ├── app.py            # Flask server, /api/ask endpoint
│   └── requirements.txt
├── frontend/
│   └── index.html        # Single-file UI
├── CLAUDE.md
├── LICENSE
├── .gitignore
└── README.md
```

## Deploy on Streamlit Community Cloud

The app also ships as a single Streamlit script (`streamlit_app.py`) that bundles the
Gemini call and the chat UI together — no separate Flask server needed, which makes it
a much better fit for [Streamlit Community Cloud](https://streamlit.io/cloud).

### Run it locally

```bash
pip install -r requirements.txt

mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml and paste in your real Gemini key

streamlit run streamlit_app.py
```

### Deploy it

1. Push this repo to GitHub (make sure `.streamlit/secrets.toml` is **not** committed —
   it's already in `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in, and click "New app."
3. Point it at this repo, branch `main`, and set the main file to `streamlit_app.py`.
4. Under **Settings → Secrets**, paste:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Deploy. Streamlit installs from `requirements.txt` automatically.

## Setup (Flask + static frontend version)

The original two-part version (Flask backend + `frontend/index.html`) still works if
you'd rather run/deploy backend and frontend separately.

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set your Gemini API key (get one at https://aistudio.google.com/apikey)
export GEMINI_API_KEY="your-key-here"   # Windows: set GEMINI_API_KEY=your-key-here

python app.py
```

The backend runs at `http://localhost:5000`.

### 2. Frontend

Just open `frontend/index.html` in your browser. It talks to the backend at `http://localhost:5000/api/ask`.

(No npm install, no build — it's a single static file.)

## How it works

1. You type a question into the input box.
2. The frontend sends a `POST` to `/api/ask` on the Flask backend.
3. The backend calls the Gemini API (`gemini-2.5-flash`) with your question.
4. The answer streams back and renders on the "board."

## Roadmap

- [ ] Conversation history / follow-up questions
- [ ] Subject tagging (Math, Physics, CS, etc.)
- [ ] Export answers as notes (Markdown/PDF)
- [ ] Deploy backend (Render/Railway) + frontend (Vercel/Netlify)

## License

MIT — see [LICENSE](./LICENSE).
