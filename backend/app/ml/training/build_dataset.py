from app.ml.training.dataset import TrainingDataset
from app.ml.training.split import split_dataset
from app.ml.training.validation import validate_dataset


def build():

    dataset = TrainingDataset()

    report = validate_dataset(
        dataset.examples
    )

    print("IdX Training Dataset")
    print("=" * 50)
    print("Examples:", len(dataset))
    print("Valid:", report.valid)

    train, validation, test = split_dataset(
        dataset.examples
    )

    print()
    print("Train:", len(train))
    print("Validation:", len(validation))
    print("Test:", len(test))


if __name__ == "__main__":
    build()
