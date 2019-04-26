"""
Author: Suraj Regmi

Data: 26th April, 2019

Description:

Contains functions for playoff estimator which estimates the probabilities for all the IPL teams going to
playoff based on the number of games played with each teams and their current point score.

Tie Case:
In case of ties that happen when more than one team have equal points and are fighting for top 4 positions, I have
assumed equal probability of making into playoffs for all the tied teams and so incorporated equal weightage.

Example:
    If both SRH and MI are on 14 points standing 4th and 5th, I assume probability of them making into playoffs as 0.5
    (for both).
"""


import json

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


results = []


def _get_data():
    """
    Returns crude data from the JSON files saved in data/ folder.
    ---------------------------
    Returns games dictionary, points table dictionary and teams map dictionary in order.
    """
    return json.load(open('data/games.json')), json.load(open('data/points_table.json')), \
           json.load(open('data/teams_map.json'))


def _preprocess_data(games, points, tmap):
    """
    Gets crude data and preprocess to the format as preferred.
    Dictionaries loaded from JSON files don't have integers as the keys so we convert the string keys into integer keys.
    """
    games = dict((int(i), dict((int(k), l) for k, l in j.items())) for i, j in games.items())
    points = dict((int(i), j) for i, j in points.items())
    tmap = dict((int(i), j) for i, j in tmap.items())
    return games, points, tmap


def get_data():
    """
    Fetches preprocessed data.
    Refer to above two functions.
    """
    games, points, tmap = _get_data()
    return _preprocess_data(games, points, tmap)


def unique_game_dictionary(games):
    """
    Removes double instances of the matches.
    """
    for i in range(8, 0, -1):
        if i == 8:
            del games[i]
            continue

        for j in range(1, i):
            del games[i][j]


def get_rem_matches(games):
    """
    Returns list of tuples of all the match instances.
    """
    rem_matches = []
    for key, value in games.items():
        rem_games = [(key, k) for k, v in value.items() for _ in range(2-v)]
        rem_matches.extend(rem_games)
    return rem_matches


def play(matches, points):
    """
    Recursively play all the match instances and append all the possible results.
    """
    if len(matches) == 0:
        results.append(points.copy())
        return

    i, j = matches.pop()

    points[i] += 2
    play(matches, points)
    points[i] -= 2

    points[j] += 2
    play(matches, points)
    points[j] -= 2

    matches.append((i, j))


def dataframize():
    """
    Convert the list of result dictionaries to the dataframe, df.
    """
    global df
    df = pd.DataFrame(results)


def get_worst_prob(key):
    """
    Gets probability of the team (key) making into playoffs assuming it has the worst run rate of the tied teams.
    """
    return sum((df[key].values.reshape(-1, 1) > df.values).sum(axis=1) > 3)/df.shape[0]


def get_nrr_prob(key):
    """
    Gets probability of the team (key) making into playoffs for just the tied games.
    """
    tie = (df[key].values.reshape(-1, 1) == df.values).sum(axis=1)
    chance = ((df[key].values.reshape(-1, 1) > df.values).sum(axis=1) < 4) & ((df[key].values.reshape(-1, 1) < df.values).sum(axis=1) < 4)
    vacant = 4 - (df[key].values.reshape(-1, 1) > df.values).sum(axis=1)
    return sum(chance * vacant / tie) / df.shape[0]


def get_estimated_prob(key):
    """
    Gets estimated probability which is the sum of worst NRR probability and only-NRR-based probability.
    """
    return get_worst_prob(key) + get_nrr_prob(key)


def get_plotting_data(tmap):
    """
    Returns the dataframe consisting of teams column and probability column.
    """
    return pd.DataFrame({'Team': [tmap[i] for i in range(1, 9)], 'Playoff Probability': [get_worst_prob(i) for i in range(1, 9)]})


def plot(folder_name, data):
    """
    Plots the bar chart and saves the PNG image inside the folder, folder_name.
    """
    plt.figure(figsize=(30, 16))

    sns.set(style="whitegrid")
    ax = sns.barplot(x="Team", y="Playoff Probability", data=data)

    ax.xaxis.label.set_size(40)
    ax.yaxis.label.set_size(40)

    for i in range(8):
        ax.xaxis.get_major_ticks()[i].label.set_fontsize(35)

    for i in range(6):
        ax.yaxis.get_major_ticks()[i].label.set_fontsize(35)

    for i in range(8):
        ax.text(i, data['Playoff Probability'][i], round(data['Playoff Probability'][i], 3), color='black', ha='center',
                fontsize=40)

    plt.savefig('{}/estimated_nrr_prob.png'.format(folder_name))


def main():
    games, points, tmap = get_data()
    unique_game_dictionary(games)
    rem_matches = get_rem_matches(games)
    play(rem_matches, points)
    dataframize()
    data = get_plotting_data(tmap)
    plot('graphs', data)


if __name__ == "__main__":
    main()
