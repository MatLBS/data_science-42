import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn import preprocessing


def standardize_data(path1, path2):
    assert isinstance(path1, str), "The first path must be a string"
    assert os.path.exists(path1), "The first file does not exist"
    assert path1.endswith(".csv"), "The first file extension must be csv"

    assert isinstance(path2, str), "The second path must be a string"
    assert os.path.exists(path2), "The second file does not exist"
    assert path2.endswith(".csv"), "The second file extension must be csv"

    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)

    knight = df2['knight']
    newdf2 = df2.drop("knight", axis='columns')

    print("------------------------Original Data------------------------")
    print(df1)
    print(df2)

    scaler = preprocessing.MinMaxScaler()
    d = scaler.fit_transform(df1)
    res1 = pd.DataFrame(d, columns=df1.columns)
    d = scaler.fit_transform(newdf2)
    res2 = pd.DataFrame(d, columns=newdf2.columns)
    res2['knight'] = knight.values

    print("------------------------Normalized Data------------------------")
    print(res1)
    print(res2)

    fig, ax = plt.subplots(1, 2, figsize=(14, 7))
    ax[0].scatter(res1['Push'], res1['Deflection'],
                  alpha=0.5, color='green', label='Knight')
    ax[0].set_xlabel("Push")
    ax[0].set_ylabel("Deflection")
    ax[0].legend(loc='upper left')

    jedi = res2[res2['knight'] == 'Jedi']
    sith = res2[res2['knight'] == 'Sith']

    ax[1].scatter(jedi['Push'], jedi['Deflection'],
                  alpha=0.5, color='blue', label='Jedi')
    ax[1].scatter(sith['Push'], sith['Deflection'],
                  alpha=0.5, color='red', label='Sith')
    ax[1].set_xlabel("Push")
    ax[1].set_ylabel("Deflection")
    ax[1].legend(loc='upper left')

    fig.suptitle('Normalized Data', fontsize=16)
    plt.tight_layout()
    plt.show()


def main():
    try:
        path1 = os.path.expanduser(
            "~/sgoinfre/Test_knight.csv"
        )
        path2 = os.path.expanduser(
            "~/sgoinfre/Train_knight.csv"
        )
        standardize_data(path1, path2)
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
