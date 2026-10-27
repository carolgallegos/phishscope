# PhishScope

Flag phishing in emails, URLs, and short messages, and show why.

Security inboxes get more suspicious mail than a person can read. PhishScope is a first pass: phishing or legitimate, plus the signals behind the call (urgent wording, mismatched links, lookalike domains).

## Status

Labeled examples live in `data/examples.csv`. `rules.check` is a first pass: urgent wording and suspicious links, with the reasons attached. `model.fit` trains a logistic regression on features from that same sheet (account wording, a bare "urgent", odd login hosts). `model.explain` lists the features that pushed each call, strongest first. The number it prints is how well that fit separates these rows, not mail it has never seen.

```bash
set PYTHONPATH=src
python -m phishscope.score
python -m phishscope.check "The urgent care clinic on campus opens at 8."
```

## Layout

- `src/phishscope` — message model, rule check, sheet classifier, and a one-off check command
- `data` — labeled examples

## Setup

Python 3.11+.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
