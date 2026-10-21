from sklearn.linear_model import LogisticRegression

from .dataset import Example, load_examples
from .features import FEATURE_NAMES, row_features
from .message import Message

# Plain reasons, one per feature, in FEATURE_NAMES order.
FEATURE_REASONS = {
    "account_phrase": "account wording",
    "prize_phrase": "prize wording",
    "urgent_word": "the word urgent",
    "suspicious_host": "a suspicious host",
    "plain_http": "a link that is not https",
    "login_on_odd_host": "a login link on an odd host",
}


def fit(examples: list[Example] | None = None) -> LogisticRegression:
    """Fit on the labeled sheet. The score is for these rows, not new mail."""
    rows = examples if examples is not None else load_examples()
    model = LogisticRegression(C=10)
    model.fit(
        [row_features(example.message) for example in rows],
        [example.label for example in rows],
    )
    return model


def predict(model: LogisticRegression, message: Message) -> str:
    return str(model.predict([row_features(message)])[0])


def explain(model: LogisticRegression, message: Message) -> tuple[str, list[str]]:
    """Return the label and the features that pushed toward it."""
    row = row_features(message)
    label = str(model.predict([row])[0])
    positive = str(model.classes_[1])
    weights = model.coef_[0]
    support: list[tuple[float, str]] = []
    opposed: list[str] = []
    for name, value, weight in zip(FEATURE_NAMES, row, weights):
        if not value:
            continue
        toward_label = weight if label == positive else -weight
        if toward_label > 0:
            support.append((toward_label, FEATURE_REASONS[name]))
        else:
            opposed.append(FEATURE_REASONS[name])
    support.sort(reverse=True)
    reasons = [text for _, text in support]
    if not reasons and opposed:
        reasons = [f"not enough on its own: {', '.join(opposed)}"]
    if not reasons:
        reasons = ["no feature fired; the base rate decided"]
    return label, reasons
