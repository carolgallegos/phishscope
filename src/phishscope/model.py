from sklearn.linear_model import LogisticRegression

from .dataset import Example, load_examples
from .features import row_features
from .message import Message


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
