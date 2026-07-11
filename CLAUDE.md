# CLAUDE.md

Guidance for Claude Code (or any AI assistant) working in this repo.

## What this project is

StudyMate AI — a small full-stack study assistant. User asks a question in a
web UI, a Flask backend forwards it to the Gemini API, the answer is
rendered back in the UI.

## Stack

There are two parallel versions of this app — keep changes to Gemini-calling
logic in sync between them when it matters:

- **`streamlit_app.py`** — the deployed version, for Streamlit Community
  Cloud. Single file, bundles UI + Gemini call. Reads the API key from
  `st.secrets` (falls back to an env var for convenience).
- **`backend/app.py` + `frontend/index.html`** — the original two-part
  version (Flask API + static HTML/JS). Useful for local dev or if the
  app ever needs a "real" separate frontend/backend split. Reads the API
  key from `.env` via `python-dotenv`.

Shared:
- **AI provider:** Google Gemini via the `google-genai` SDK, model
  `gemini-2.5-flash`
- **No frontend build tooling anywhere.** No bundler, no framework
  dependency, unless explicitly asked.
- **No database yet.** State is in-memory / session-only. If we add
  persistence, default to SQLite before reaching for anything heavier.

## Conventions

### Commits

This repo uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(<optional scope>): <description>

feat: add /api/ask endpoint
fix: handle empty prompt on frontend
docs: update README setup steps
chore: add .gitignore
refactor: extract Gemini client into its own module
```

Common types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `style`.
Keep the subject line under ~72 characters, imperative mood ("add", not
"added" or "adds").

### Python

- Keep functions small and single-purpose.
- Read secrets (API keys) from environment variables only — never hardcode
  a key, never commit one.
- Prefer explicit error handling around the Gemini API call (network
  errors, empty responses) over letting exceptions bubble to the user as a
  raw 500.

### Frontend

- Keep it a single `index.html` unless the project explicitly grows past
  that (e.g. multiple pages). Vanilla JS, no framework, until there's a
  concrete reason to add one.
- Backend URL should be a single constant at the top of the script, not
  hardcoded in multiple places.

### Secrets

`GEMINI_API_KEY` is read via `os.environ`. Never commit a `.env` file or
paste a real key into any file in this repo — `.gitignore` already excludes
`.env`.

## What to help with

- Reviewing/critiquing docs (README, this file) for clarity and gaps.
- Extending `backend/app.py` (new endpoints, error handling, streaming).
- Iterating on `frontend/index.html` (UI, UX, accessibility).
- Keeping commit messages Conventional-Commits-compliant when asked to
  draft or review commits.

## What NOT to do

- Don't add authentication, a database, or a build system unless asked —
  keep the project's current scope intact.
- Don't hardcode API keys anywhere, including in example code or comments.
