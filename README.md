# 🌍 Multilingual Money Changer

A Streamlit app that converts currencies using **GitHub Models (gpt-4o-mini)** for natural language understanding and **ExchangeRate-API** for live rates. LangSmith tracing is included.

---

## How it works

```
User types natural language  →  gpt-4o-mini (GitHub Models)
        ↓ function calling
Exchange Rate API  →  result displayed in Streamlit
```

---

## Secrets you need (2 required, 1 optional)

| Secret | Where to get it | Required? |
|--------|----------------|-----------|
| `GITHUB_TOKEN` | [github.com/settings/tokens](https://github.com/settings/tokens) — tick **"GitHub Models"** | ✅ Yes |
| `EXCHANGERATE_API_KEY` | [exchangerate-api.com](https://www.exchangerate-api.com) — free signup | ✅ Yes |
| `LANGCHAIN_API_KEY` | [smith.langchain.com](https://smith.langchain.com) | ❌ Optional |

---

## Option A — Run in GitHub Codespaces (recommended)

1. **Fork or push this repo to your GitHub account.**

2. **Add Codespaces Secrets** (so they're injected automatically):
   - Go to `github.com/settings/codespaces`
   - Click **New secret** for each:
     - `GITHUB_TOKEN`
     - `EXCHANGERATE_API_KEY`
     - `LANGCHAIN_API_KEY` *(optional)*
   - Under **Repository access**, select your repo.

3. **Open Codespaces**:
   - On your repo page → green **Code** button → **Codespaces** tab → **Create codespace on main**
   - Dependencies install automatically via `postCreateCommand`.

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```
   Codespaces will open a browser tab automatically on port 8501.

---

## Option B — Run locally

1. **Clone the repo**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/multilingual-money-changer.git
   cd multilingual-money-changer
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Mac/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up secrets**:
   ```bash
   cp .env.example .env
   # Edit .env and fill in your keys
   ```

5. **Run**:
   ```bash
   streamlit run app.py
   ```
   Open [http://localhost:8501](http://localhost:8501)

---

## GitHub repository structure

```
multilingual-money-changer/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── .env.example              # Secret key template (safe to commit)
├── .gitignore                # Excludes .env and cache files
├── .devcontainer/
│   └── devcontainer.json     # Codespaces auto-setup config
└── README.md
```

---

## Example queries

- `Convert 500 USD to AED`
- `How much is 1000 EUR in INR?`
- `كم يساوي 200 دولار بالدرهم؟` *(Arabic)*
- `100ドルを円に換算して` *(Japanese)*

---

## Notes

- The **GitHub Token** acts as your API key for GitHub Models — it replaces a paid OpenAI key.
- The free ExchangeRate-API tier gives 1,500 requests/month — more than enough for demos.
- LangSmith tracing is optional; if `LANGCHAIN_API_KEY` is not set, tracing simply won't log.
