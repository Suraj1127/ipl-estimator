"""
Author: Suraj Regmi
Date: 27th April, 2019
Description: Module to generate graphs of the progress of all the IPL Teams.
"""

import json

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_data():
    return json.load(open('data/progress.json'))


def preprocess(data):
    """
    Convert the progress data dictionary into preferred custom format (dataframe) for graphing purpose.
    """
    data = dict((i, list(map(int, list(j)))) for i, j in data.items())
    progress = dict((i, [2*sum(j[0:k+1]) for k, l in enumerate(j)]) for i, j in data.items())
    progress_df = pd.DataFrame([(i, k+1, l) for i, j in progress.items() for k, l in enumerate(j)], columns=['Team', 'Game', 'Points'])
    return progress_df


def plot_progress():
    """
    Plot the progress for all the IPL teams and saves the line chart inside data folder as ipl_progress.png.
    """
    data = get_data()
    progress_df = preprocess(data)

    sns.set(style="whitegrid", font_scale=4)

    ax = sns.catplot(x="Game", y="Points", hue="Team", data=progress_df, kind='point', height=16, aspect=30/16, s=10, scale=2)
    plt.savefig('graphs/ipl_progress.png')


if __name__ == "__main__":
    plot_progress()