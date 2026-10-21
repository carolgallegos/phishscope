from .dataset import Example, load_examples
from .model import explain, fit, predict
from .rules import check


def _tally(rows: list[Example], label_of) -> dict:
    misses: list[str] = []
    correct = 0
    for example in rows:
        label = label_of(example)
        if label == example.label:
            correct += 1
            continue
        misses.append(
            f"expected {example.label}, got {label}: {example.message.text}"
        )
    return {"correct": correct, "total": len(rows), "misses": misses}


def score(examples: list[Example] | None = None) -> dict:
    rows = examples if examples is not None else load_examples()
    return _tally(rows, lambda example: check(example.message)[0])


def score_model(examples: list[Example] | None = None) -> dict:
    rows = examples if examples is not None else load_examples()
    model = fit(rows)
    return _tally(rows, lambda example: predict(model, example.message))


def main() -> None:
    rules = score()
    rows = load_examples()
    learned = score_model(rows)
    print(f"rules {rules['correct']}/{rules['total']}")
    print(f"model {learned['correct']}/{learned['total']}")
    for miss in learned["misses"]:
        print(miss)
    model = fit(rows)
    for example in rows:
        label, reasons = explain(model, example.message)
        print(f"{label}: {'; '.join(reasons)}")
        print(f"  {example.message.text}")


if __name__ == "__main__":
    main()
