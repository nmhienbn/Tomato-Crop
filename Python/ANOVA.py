from scipy.stats import f_oneway
import numpy as np
from scipy.stats import studentized_range
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import networkx as nx


def calculate_mse(data):
    # Calculate sum of squares within (SSW) and degrees of freedom within (dfw)
    ssw = sum(np.sum((group - np.mean(group)) ** 2) for group in data)
    dfw = sum(len(group) - 1 for group in data)

    # Calculate Mean Square Error (MSE)
    mse = ssw / dfw

    return mse


def perform_anova(data, alpha=0.05):
    # Perform ANOVA test
    f_statistic, p_value = f_oneway(*data)

    charGroup = [""] * len(data)
    # Check the significance level
    if p_value < alpha:
        # Reject the null hypothesis: Significant differences between group means.
        # Calculate MSE, and dfw
        mse = calculate_mse(data)
        n_per_group = len(data[0])

        # Extract Turkey's HSD values
        q_crit = studentized_range.ppf(1 - alpha, 12, 10 * 12 - 12)

        lsd = q_crit * np.sqrt(2 * mse / n_per_group)

        charGroup = TurkeyHSD(data, lsd)
        lsd = round(lsd, 2)
    else:
        lsd = "ns"
    return lsd, charGroup


def find_maximal_cliques(edges):
    G = nx.Graph(edges)
    cliques = list(nx.find_cliques(G))

    # Sort each clique individually
    sorted_cliques = [sorted(clique) for clique in cliques]

    # Sort all cliques alphabetically
    sorted_cliques.sort()

    return sorted_cliques


def TurkeyHSD(data, lsd):
    # Perform Tukey's HSD test
    mean = [np.mean(group) for group in data]

    significant_pairs = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if np.abs(np.mean(data[i]) - np.mean(data[j])) < lsd:
                significant_pairs.append((i, j))

    # Find maximal cliques
    maximal_cliques = find_maximal_cliques(significant_pairs)
    charGroup = [""] * len(data)
    current_letter = "a"
    # Set the character group
    for clique in maximal_cliques:
        if len(clique) > 1:
            for index in clique:
                charGroup[index] += current_letter
            current_letter = chr(ord(current_letter) + 1)
    return charGroup
