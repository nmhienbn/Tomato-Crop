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


def getLabels(groups_mean: list, groups_size: list, q_crit: float, msw: float):
    # Perform Tukey's HSD test

    significant_pairs = []
    is_all = True
    for i in range(len(groups_mean)):
        for j in range(i + 1, len(groups_mean)):
            lsd = q_crit * np.sqrt(msw / 2 * (1 / groups_size[i] + 1 / groups_size[j]))
            # print(lsd)
            if np.abs(groups_mean[i] - groups_mean[j]) < lsd:
                significant_pairs.append((i, j))
            else:
                is_all = False

    charGroup = [""] * len(groups_mean)
    if is_all:
        return charGroup

    # Find maximal cliques
    maximal_cliques = find_maximal_cliques(significant_pairs)
    current_letter = "a"
    # Set the character group
    for clique in maximal_cliques:
        for index in clique:
            charGroup[index] += current_letter
        current_letter = chr(ord(current_letter) + 1)
    for i in range(len(charGroup)):
        if charGroup[i] == "":
            charGroup[i] += current_letter
            current_letter = chr(ord(current_letter) + 1)
    return charGroup


# function to convert to superscript
def get_superscript(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans("".join(normal), "".join(super_s))
    return x.translate(res)


# function to convert to subscript
def get_subscript(x):
    normal = "0123456789+-=()."
    sub_s = "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎."
    res = x.maketrans("".join(normal), "".join(sub_s))
    return x.translate(res)
