import pandas as pd
import matplotlib.pyplot as plt
import os


def draw_graphs_test(path):
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"

    data = pd.read_csv(path)
    fig, ax = plt.subplots(1, 2, figsize=(14, 7))

    ax[0].scatter(data['Empowered'], data['Stims'],
                  alpha=0.5, color='green', label='Knight')
    ax[0].set_xlabel("Empowered")
    ax[0].set_ylabel("Stims")
    ax[0].legend()

    ax[1].scatter(data['Push'], data['Deflection'],
                  alpha=0.5, color='green', label='Knight')
    ax[1].set_xlabel("Push")
    ax[1].set_ylabel("Deflection")
    ax[1].set_ylim(0, 0.08)
    ax[1].legend()

    fig.suptitle('Test Knight Histograms', fontsize=16)
    plt.tight_layout()
    plt.show()


def draw_graphs_train(path):
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"

    data = pd.read_csv(path)
    fig, ax = plt.subplots(1, 2, figsize=(14, 7))
    jedi = data[data['knight'] == 'Jedi']
    sith = data[data['knight'] == 'Sith']

    ax[0].scatter(jedi['Empowered'], jedi['Stims'],
                  alpha=0.5, color='blue', label='Jedi')
    ax[0].scatter(sith['Empowered'], sith['Stims'],
                  alpha=0.5, color='red', label='Sith')
    ax[0].set_xlabel("Empowered")
    ax[0].set_ylabel("Stims")
    ax[0].legend()

    ax[1].scatter(jedi['Push'], jedi['Deflection'],
                  alpha=0.5, color='blue', label='Jedi')
    ax[1].scatter(sith['Push'], sith['Deflection'],
                  alpha=0.5, color='red', label='Sith')
    ax[1].set_xlabel("Push")
    ax[1].set_ylabel("Deflection")
    ax[1].set_ylim(0, 0.08)
    ax[1].legend()

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
