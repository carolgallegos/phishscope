import argparse
import sys

from .message import Message
from .model import explain, fit
from .rules import check


def _kind_from_text(text: str, kind: str | None) -> str:
    if kind:
        return kind
    stripped = text.strip()
    if stripped.startswith("http://") or stripped.startswith("https://"):
        return "url"
    return "email"


def inspect(text: str, kind: str | None = None) -> None:
    message = Message(text=text, kind=_kind_from_text(text, kind))
    rule_label, rule_reasons = check(message)
    print("rules", rule_label)
    if rule_reasons:
        for reason in rule_reasons:
            print(" ", reason)
    else:
        print("  nothing fired")
    model_label, model_reasons = explain(fit(), message)
    print("model", model_label)
    for reason in model_reasons:
        print(" ", reason)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check one email, URL, or chat against the rules and the sheet model."
    )
    parser.add_argument("text", nargs="?", help="the message to check")
    parser.add_argument(
        "--kind",
        choices=("email", "url", "chat"),
        help="defaults to url if the text starts with http, else email",
    )
    args = parser.parse_args(argv)
    if not args.text:
        parser.print_help()
        return 2
    inspect(args.text, args.kind)
    return 0


if __name__ == "__main__":
    sys.exit(main())
