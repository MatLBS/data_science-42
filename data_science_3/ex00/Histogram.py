import pandas as pd
import matplotlib.pyplot as plt
import os


def draw_graphs_test(path):
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"

    data = pd.read_csv(path)
    columns = data.columns

    fig, ax = plt.subplots(6, 5, figsize=(14, 10))
    k = 0

    for i in range(6):
        for j in range(5):
            ax[i][j].hist(data[columns[k]], 50, density=False,
                          color='green', alpha=0.7, label='knight')
            ax[i][j].set_title(columns[k], fontsize=10)
            ax[i][j].legend()
            k += 1
    fig.suptitle('Test Knight Histograms', fontsize=16)
    plt.tight_layout()
    plt.show()


def draw_graphs_train(path):
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"

    data = pd.read_csv(path)
    columns = data.columns

    fig, ax = plt.subplots(6, 5, figsize=(14, 10))
    k = 0
    jedi = data[data['knight'] == 'Jedi']
    sith = data[data['knight'] == 'Sith']

    for i in range(6):
        for j in range(5):
            ax[i][j].hist(jedi[columns[k]], bins=50,
                          alpha=0.6, label='Jedi', color='blue')
            ax[i][j].hist(sith[columns[k]], bins=50,
                          alpha=0.6, label='Sith', color='red')
            ax[i][j].set_title(columns[k], fontsize=10)
            ax[i][j].legend()
            k += 1
    fig.suptitle('Train Knight Histograms', fontsize=16)
    plt.tight_layout()
    plt.show()


def main():
    try:
        path = os.path.expanduser(
            "~/sgoinfre/Test_knight.csv"
        )
        draw_graphs_test(path)
        path = os.path.expanduser(
            "~/sgoinfre/Train_knight.csv"
        )
        draw_graphs_train(path)
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
