import os

from matplotlib import pyplot as plt


def plot_result(cfg, x_train, x_validation, train, validation, xlabel, ylabel, legend, title, save: bool, plot: bool, log: bool, filename: str = None):
    if not os.path.exists(cfg.saveDirFigs):
        os.makedirs(cfg.saveDirFigs)

    fig = plt.figure(figsize=(1.61 * cfg.figSize, 1 * cfg.figSize))
    plt.plot(x_train, train, color='#01256E', linewidth=cfg.lineWidth, marker=cfg.markerShape,
             markersize=cfg.markerSize)
    plt.plot(x_validation, validation, color='#95001A', linewidth=cfg.lineWidth, marker=cfg.markerShape,
             markersize=cfg.markerSize)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend(legend)
    plt.title(title)
    if log:
        plt.yscale("log")
    if save:
        path_to_save = os.path.join(cfg.saveDirFigs, filename + ".png")
        fig.savefig(path_to_save, bbox_inches='tight')
    if plot:
        plt.show()
    else:
        plt.clf()
        fig.clf()



from typing import List, Optional

import numpy as np
from sklearn.metrics import confusion_matrix

def print_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: Optional[List] = None,
    hide_zeroes: bool = False,
    hide_diagonal: bool = False,
    hide_threshold: Optional[float] = None,
    print_cm = False
):
    """Print a nicely formatted confusion matrix with labelled rows and columns.

    Predicted labels are in the top horizontal header, true labels on the vertical header.

    Args:
        y_true (np.ndarray): ground truth labels
        y_pred (np.ndarray): predicted labels
        labels (Optional[List], optional): list of all labels. If None, then all labels present in the data are
            displayed. Defaults to None.
        hide_zeroes (bool, optional): replace zero-values with an empty cell. Defaults to False.
        hide_diagonal (bool, optional): replace true positives (diagonal) with empty cells. Defaults to False.
        hide_threshold (Optional[float], optional): replace values below this threshold with empty cells. Set to None
            to display all values. Defaults to None.
    """
    if labels is None:
        labels = np.unique(np.concatenate((y_true, y_pred)))
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    if print_cm:
        # find which fixed column width will be used for the matrix
        columnwidth = max(
            [len(str(x)) for x in labels] + [5]
        )  # 5 is the minimum column width, otherwise the longest class name
        empty_cell = ' ' * columnwidth

        # top-left cell of the table that indicates that top headers are predicted classes, left headers are true classes
        padding_fst_cell = (columnwidth - 3) // 2  # double-slash is int division
        fst_empty_cell = padding_fst_cell * ' ' + 't/p' + ' ' * (columnwidth - padding_fst_cell - 3)

        # Print header
        print('    ' + fst_empty_cell, end=' ')
        for label in labels:
            print(f'{label:{columnwidth}}', end=' ')  # right-aligned label padded with spaces to columnwidth

        print()  # newline
        # Print rows
        for i, label in enumerate(labels):
            print(f'    {label:{columnwidth}}', end=' ')  # right-aligned label padded with spaces to columnwidth
            for j in range(len(labels)):
                # cell value padded to columnwidth with spaces and displayed with 1 decimal
                cell = f'{cm[i, j]:{columnwidth}.1f}'
                if hide_zeroes:
                    cell = cell if float(cm[i, j]) != 0 else empty_cell
                if hide_diagonal:
                    cell = cell if i != j else empty_cell
                if hide_threshold:
                    cell = cell if cm[i, j] > hide_threshold else empty_cell
                print(cell, end=' ')
            print()
    return cm