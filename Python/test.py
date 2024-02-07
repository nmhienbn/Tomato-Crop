from statsmodels.stats.multicomp import pairwise_tukeyhsd
import numpy as np

# Given data
data = [
    [
        0.75,
        0.7,
        0.65,
        0.75,
        0.8,
        0.8,
        0.75,
        0.85,
        0.85,
        0.75,
        0.8,
        0.7,
        0.6,
        0.7,
        0.7,
        0.7,
        0.7,
        0.6,
        0.8,
        0.6,
    ],
    [
        0.75,
        0.8,
        0.7,
        0.7,
        0.75,
        0.8,
        0.8,
        0.7,
        0.8,
        0.75,
        0.7,
        0.8,
        0.8,
        0.75,
        0.8,
        0.7,
        0.7,
        0.8,
        0.7,
        0.8,
    ],
    [
        0.8,
        0.8,
        0.8,
        0.7,
        0.7,
        0.7,
        0.65,
        0.8,
        0.5,
        0.7,
        0.9,
        0.8,
        0.7,
        0.7,
        0.5,
        0.8,
        0.8,
        0.8,
        0.8,
        0.8,
    ],
    [
        0.7,
        0.7,
        0.75,
        0.75,
        0.7,
        0.7,
        0.7,
        0.8,
        0.7,
        0.75,
        0.8,
        0.9,
        0.7,
        0.75,
        0.75,
        0.8,
        0.8,
        0.7,
        0.6,
        0.5,
    ],
    [
        0.7,
        0.7,
        0.71,
        0.75,
        0.9,
        0.85,
        0.7,
        0.6,
        0.9,
        0.7,
        0.8,
        0.7,
        0.7,
        0.8,
        0.7,
        0.8,
        0.8,
        0.7,
        0.8,
        0.7,
    ],
    [
        0.7,
        0.7,
        0.7,
        0.7,
        0.6,
        0.7,
        0.75,
        0.7,
        0.7,
        0.7,
        0.7,
        0.75,
        0.7,
        0.5,
        0.72,
        0.5,
        0.7,
        0.76,
        0.55,
        0.7,
    ],
    [
        0.7,
        0.8,
        0.7,
        1,
        0.7,
        0.65,
        0.7,
        0.65,
        0.7,
        0.5,
        0.9,
        0.8,
        0.8,
        0.6,
        0.5,
        0.8,
        0.8,
        0.8,
        0.6,
        0.7,
    ],
    [
        0.9,
        0.8,
        0.65,
        0.8,
        0.65,
        0.8,
        0.7,
        0.7,
        0.75,
        0.7,
        0.6,
        0.8,
        0.65,
        0.8,
        0.75,
        0.8,
        0.7,
        0.75,
        0.7,
        0.7,
    ],
    [
        1,
        0.75,
        0.7,
        0.75,
        0.7,
        0.7,
        0.75,
        0.7,
        0.7,
        0.8,
        0.5,
        0.6,
        0.7,
        0.7,
        0.6,
        0.6,
        0.8,
        0.6,
        0.8,
        0.8,
    ],
    [
        0.7,
        0.7,
        0.7,
        0.7,
        0.7,
        0.8,
        0.75,
        0.75,
        0.7,
        0.7,
        0.7,
        0.7,
        0.8,
        0.8,
        0.7,
        0.75,
        0.75,
        0.75,
        0.6,
        0.7,
    ],
    [
        0.7,
        0.7,
        0.7,
        0.5,
        0.75,
        0.6,
        0.7,
        0.7,
        0.8,
        0.4,
        0.65,
        0.75,
        0.65,
        0.7,
        0.7,
        0.7,
        0.65,
        0.5,
        0.6,
        0.6,
    ],
    [
        0.6,
        0.7,
        0.7,
        0.4,
        0.5,
        0.6,
        0.75,
        0.75,
        0.6,
        0.6,
        0.6,
        0.7,
        0.7,
        0.7,
        0.6,
        0.65,
        0.65,
        0.7,
        0.6,
        0.5,
    ],
]

import ANOVA

print(ANOVA.perform_anova(data))
