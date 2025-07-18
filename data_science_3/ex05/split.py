import pandas as pd
from sklearn.model_selection import train_test_split
import sys
import os


def split_data(path):
    assert isinstance(path, str), "The first path must be a string"
    assert os.path.exists(path), "The first file does not exist"
    assert path.endswith(".csv"), "The first file extension must be csv"

    df = pd.read_csv(path)

    # split the dataset
    train, val = train_test_split(
        df, test_size=0.2, random_state=0)

    train.to_csv("Training_knight.csv", index=False)
    val.to_csv("Validation_knight.csv", index=False)


def main():
    try:
        n = len(sys.argv)
        assert n == 2, "Please provide one argument!"
        split_data(sys.argv[1])
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
