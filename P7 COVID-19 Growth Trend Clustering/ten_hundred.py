'''
Evan Hansen
CS 540
P7: COVID-19 Growth Trend Clustering
'''

import csv
import numpy as np
from datetime import date
import scipy.cluster.hierarchy as sci
from matplotlib import pyplot as plt


def load_data(filepath):
    dict_list = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            del row['Lat']
            del row['Long']
            dict_list.append(row)
    return dict_list


# x is days between n/10 and n cases
# y is days between n/100 and n/10 cases
def calculate_x_y(time_series):
    # [0] is date, [1] is # of cases
    time_list = list(time_series.items())
    time_list.reverse()
    n_p = time_list[0]
    if int(n_p[1]) == 0:
        return None, None
    n_10_p = None
    n_100_p = None

    # find n/10 days
    found_10 = False
    for day in time_list:
        # skips country and region
        if not day[1].isdigit():
            continue
        if not found_10 and int(day[1]) <= int(n_p[1]) / 10:
            n_10_p = day
            found_10 = True

        if int(day[1]) <= int(n_p[1]) / 100:
            n_100_p = day
            break

    x = None
    y = None
    if n_10_p is not None:
        x = (format_date(n_p[0]) - format_date(n_10_p[0])).days

    if n_100_p is not None:
        y = (format_date(n_10_p[0]) - format_date(n_100_p[0])).days

    return x, y


def format_date(day):
    li = list(map(int, day.split('/')))
    d = date(li[2], li[0], li[1])

    return d


# Must filter out None Values of (x,y)
def hac(dataset):
    # filter NaN values
    cull_list = []
    for feature in dataset:
        if type(feature[0]) is not int or type(feature[1]) is not int:
            cull_list.append(feature)
    for item in cull_list:
        dataset.remove(item)

    m = len(dataset)

    # Copy of dataset to be modified
    clusters = [[i] for i in dataset]

    # Z = sci.linkage(dataset)
    # fig = plt.figure(figsize=(25, 10))
    # dn = sci.dendrogram(Z)
    # plt.show()
    # clusters = sorted(clusters, key=lambda x: (x[0][0], x[0][1]))

    # [0] & [1] are merged clusters, [2] is distance between clusters,
    # [3] is original observations in cluster
    # dataset index is original cluster numbers
    z = [[0, 0, 0, 0] for i in range((m - 1))]

    global_best = 0
    for row in z:
        p, ind, dist = closest_cluster(clusters, global_best)
        clusters.append(p[0] + p[1])
        clusters[ind[0]] = None
        clusters[ind[1]] = None

        # Format output
        row[0] = ind[0]
        row[1] = ind[1]
        row[2] = dist
        row[3] = len(clusters[-1])

        # because it sorts on min dist
        # once global best is achieved, search can terminate
        global_best = dist

    return np.asarray(z)


def closest_cluster(clusters, global_best):
    min_dist = float('inf')
    pair = ()
    index = ()
    for i in range(len(clusters)):
        src = clusters[i]
        if src is None:
            continue
        for j in range(i + 1, len(clusters)):
            tar = clusters[j]
            if tar is None:
                continue
            dist = cluster_dist(src, tar, global_best)
            if dist < min_dist:
                min_dist = dist
                pair = (src, tar)
                index = (i, j)

                # Speeds up checking
                if min_dist <= global_best:
                    return pair, index, min_dist

    return pair, index, min_dist


def cluster_dist(src, tar, global_best):
    min_dist = float('inf')
    for i in range(len(src)):
        e1 = src[i]
        for j in range(len(tar)):
            e2 = tar[j]
            # if equal, dist = 0
            if e1 == e2:
                return 0

            dist = np.linalg.norm(np.subtract(e2, e1))
            if dist < min_dist:
                min_dist = dist

            if min_dist <= global_best:
                return min_dist

    return min_dist


if __name__ == "__main__":
    series = load_data('time_series_covid19_confirmed_global.csv')
    feature_matrix = []
    for country in series:
        xy_pair = list(calculate_x_y(country))
        feature_matrix.append(xy_pair)

    Z = hac(feature_matrix)
    fig = plt.figure(figsize=(25, 10))
    dn = sci.dendrogram(Z)
    plt.show()
