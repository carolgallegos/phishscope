import re

from .message import Message

ACCOUNT = (
    "verify your",
    "suspended",
    "one-time code",
    "act now",
    "pay the fee",
)

PRIZE = (
    "gift card",
    "you won",
)

SUSPICIOUS_HOSTS = (
    "paypa1",
    ".xyz",
    ".top",
    ".buzz",
    ".ru/",
)

FEATURE_NAMES = (
    "account_phrase",
    "prize_phrase",
    "urgent_word",
    "suspicious_host",
    "plain_http",
    "login_on_odd_host",
)

_HOST = re.compile(r"https?://([^/\s]+)", re.IGNORECASE)
_URGENT = re.compile(r"\burgent\b", re.IGNORECASE)


def _odd_login_host(host: str) -> bool:
    name = host.split(":")[0].lower().rstrip(".")
    if name.endswith(".edu") or name.endswith(".gov"):
        return False
    stem = name.rsplit(".", 1)[0]
    return "-" in stem or "portal" in stem


def row_features(message: Message) -> list[float]:
    text = message.text.lower()
    hosts = _HOST.findall(message.text)
    linked = "http://" in text or "https://" in text or message.kind == "url"
    suspicious = linked and any(host in text for host in SUSPICIOUS_HOSTS)
    sign_in = "login" in text or "sign in" in text
    odd_login = sign_in and any(_odd_login_host(host) for host in hosts)
    values = {
        "account_phrase": any(phrase in text for phrase in ACCOUNT),
        "prize_phrase": any(phrase in text for phrase in PRIZE),
        "urgent_word": _URGENT.search(message.text) is not None,
        "suspicious_host": suspicious,
        "plain_http": "http://" in text and "https://" not in text,
        "login_on_odd_host": odd_login,
    }
    return [float(values[name]) for name in FEATURE_NAMES]
