import numpy as np
from sklearn.metrics import confusion_matrix,classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import sys


def draw_matrix(prediction, truth):
    data_prediction = open(prediction).read().split('\n')
    data_truth = open(truth).read().split('\n')

    predicted = np.array(data_prediction)
    actual = np.array(data_truth)

    cm = confusion_matrix(actual,predicted)
    sns.heatmap(cm, 
            annot=True,
            fmt='g', 
            xticklabels=['0','1'],
            yticklabels=['0','1'],
            cmap="viridis")
    plt.ylabel('Actual', fontsize=13)
    plt.gca().xaxis.set_label_position('top') 
    plt.xlabel('Prediction', fontsize=13)
    plt.gca().xaxis.tick_top()

    plt.gca().figure.subplots_adjust(bottom=0.2)
    plt.gca().figure.text(0.5, 0.05, 'Confusion Matrix', ha='center', fontsize=13)

    print(classification_report(actual, predicted))
    print(cm)
    plt.show()


def main():
    try:
        n = len(sys.argv)
        assert n == 3, "Please provide two arguments!"
        draw_matrix(sys.argv[1], sys.argv[2])
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
