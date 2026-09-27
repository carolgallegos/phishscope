from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    """One item to check: an email body, a URL, or a short chat message."""

    text: str
    kind: str

    def __post_init__(self) -> None:
        if self.kind not in {"email", "url", "chat"}:
            raise ValueError("kind must be email, url, or chat")
        if not self.text.strip():
            raise ValueError("text is empty")
