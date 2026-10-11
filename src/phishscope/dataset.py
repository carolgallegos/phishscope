import csv
from dataclasses import dataclass
from pathlib import Path

from .message import Message

LABELS = {"phishing", "legitimate"}


@dataclass(frozen=True)
class Example:
    message: Message
    label: str


def examples_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "examples.csv"


def load_examples(path: Path | None = None) -> list[Example]:
    source = path or examples_path()
    rows: list[Example] = []
    with source.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            label = row["label"].strip()
            if label not in LABELS:
                raise ValueError(f"unknown label: {label}")
            rows.append(Example(Message(text=row["text"], kind=row["kind"].strip()), label))
    return rows
