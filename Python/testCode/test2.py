from statsmodels.stats.multicomp import pairwise_tukeyhsd
import numpy as np

# Given data
data = [
    [7, 7, 15, 11, 9, 10],
    [12, 17, 12, 18, 18, 16],
    [14, 18, 18, 19, 19, 17],
    [19, 25, 22, 19, 23, 24],
    [7, 10, 11, 15, 11, 14],
]

import ANOVA

print(ANOVA.perform_anova(data))
