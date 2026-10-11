# PhishScope

Flag phishing in emails, URLs, and short messages, and show why.

Security inboxes get more suspicious mail than a person can read. PhishScope is a first pass: phishing or legitimate, plus the signals behind the call (urgent wording, mismatched links, lookalike domains).

## Status

Labeled examples live in `data/examples.csv`. `rules.check` is a first pass: urgent wording and suspicious links, with the reasons attached.

## Layout

- `src/phishscope` — message model and, later, the checker
- `data` — labeled examples

## Setup

Python 3.11+.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
