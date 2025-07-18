import pandas as pd
import os
import scipy.stats


def calculate_corr(path):
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"

    data = pd.read_csv(path)
    columns = data.columns

    y = [1 if data.loc[i]['knight'] == 'Jedi' else 0 for i in range(len(data))]
    for i in range(len(columns)):
        if columns[i] == 'knight':
            print(f"{columns[i]}: 1.000000")
        else:
            x = data[columns[i]]
            corr = scipy.stats.pearsonr(x, y)
            print(f"{columns[i]}: {round(corr[0], 6)}")


def main():
    try:
        path = os.path.expanduser(
            "~/sgoinfre/Train_knight.csv"
        )
        calculate_corr(path)
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
