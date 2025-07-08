import pandas as pd
import matplotlib.pyplot as plt
import os

def draw_graphs_knights(path):
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"

    data = pd.read_csv(path)
    print(data.columns)
    columns = data.columns




def main():
    try:
        path = os.path.expanduser(
            "~/sgoinfre/Test_knight.csv"
        )
        draw_graphs_knights(path)
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
