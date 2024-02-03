import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import networkx as nx


def find_maximal_cliques(edges):
    G = nx.Graph(edges)
    cliques = list(nx.find_cliques(G))

    # Sort each clique individually
    sorted_cliques = [sorted(clique) for clique in cliques]

    # Sort all cliques alphabetically
    sorted_cliques.sort()

    return sorted_cliques


def getLabels(groups_mean, lsd):
    # Perform Tukey's HSD test

    significant_pairs = []
    for i in range(len(groups_mean)):
        for j in range(i + 1, len(groups_mean)):
            if np.abs(groups_mean[i] - groups_mean[j]) < lsd:
                significant_pairs.append((i, j))

    # Find maximal cliques
    maximal_cliques = find_maximal_cliques(significant_pairs)
    charGroup = [""] * len(groups_mean)
    current_letter = "a"
    # Set the character group
    for clique in maximal_cliques:
        if len(clique) > 1:
            for index in clique:
                charGroup[index] += current_letter
            current_letter = chr(ord(current_letter) + 1)
    return charGroup