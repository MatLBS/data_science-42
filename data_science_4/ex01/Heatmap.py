import numpy as np
from sklearn.metrics import confusion_matrix,classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd


def draw_heatmap(path):
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"
    
    df = pd.read_csv(path)

    hm = sns.heatmap(df)
    plt.show()



def main():
    try:
        path = os.path.expanduser(
            "~/sgoinfre/Train_knight.csv"
        )
        draw_heatmap(path)
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
