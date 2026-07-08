# ProCheck-ResumeAI

An AI-powered ATS (Applicant Tracking System) resume analyzer built with Django. Upload a PDF resume, paste a job description, and get a detailed compatibility score using NLP and semantic analysis.

## Stack

- **Backend**: Django 6.x, SQLite
- **NLP/ML**: spaCy (`en_core_web_sm`), NLTK, scikit-learn, sentence-transformers (`all-MiniLM-L6-v2`), PyTorch
- **PDF parsing**: pdfplumber, pdfminer.six, PyPDF2
- **Frontend**: Tailwind CSS (CDN), Chart.js

## How to run

```
python manage.py runserver 0.0.0.0:5000
```

The configured workflow ("Start application") runs this automatically on port 5000.

## First-time setup (already done)

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
python manage.py migrate
```

## Environment variables

| Variable | Purpose |
|---|---|
| `SESSION_SECRET` | Django `SECRET_KEY` (falls back to insecure default if not set) |
| `DEBUG` | Set to `False` in production |

## Scoring model

The ATS score is a weighted composite:
- **Keyword score** (TF-IDF similarity) — 30%
- **Semantic score** (sentence-transformers cosine similarity) — 25%
- **Skills match** (cross-reference against 200+ skill library) — 20%
- **Formatting/structure score** — 25%

## User preferences

- Keep existing project structure (Django apps: `accounts`, `analyzer`, `core`)
- Use SQLite for development; no external database required
