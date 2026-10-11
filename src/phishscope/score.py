from .dataset import Example, load_examples
from .rules import check


def score(examples: list[Example] | None = None) -> dict:
    rows = examples if examples is not None else load_examples()
    misses: list[str] = []
    correct = 0
    for example in rows:
        label, reasons = check(example.message)
        if label == example.label:
            correct += 1
            continue
        misses.append(
            f"expected {example.label}, got {label}: {example.message.text}"
        )
    total = len(rows)
    return {"correct": correct, "total": total, "misses": misses}


def main() -> None:
    result = score()
    print(f"{result['correct']}/{result['total']}")
    for miss in result["misses"]:
        print(miss)


if __name__ == "__main__":
    main()
