from .message import Message

URGENT = (
    "verify your",
    "suspended",
    "one-time code",
    "act now",
    "urgent",
    "gift card",
    "you won",
    "pay the fee",
)

SUSPICIOUS_HOSTS = (
    "paypa1",
    ".xyz",
    ".top",
    ".buzz",
    ".ru/",
)


def check(message: Message) -> tuple[str, list[str]]:
    """Return phishing or legitimate, plus the signals that fired."""
    text = message.text.lower()
    reasons: list[str] = []

    for phrase in URGENT:
        if phrase in text:
            reasons.append(f"urgent wording: {phrase}")

    if "http://" in text or message.kind == "url":
        for host in SUSPICIOUS_HOSTS:
            if host in text:
                reasons.append(f"suspicious link: {host}")

    if "http://" in text and "https://" not in text and message.kind != "url":
        reasons.append("link is not https")

    label = "phishing" if reasons else "legitimate"
    return label, reasons
