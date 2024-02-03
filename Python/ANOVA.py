from scipy.stats import f_oneway, t
import numpy as np
from scipy.stats import studentized_range


def calculate_mse(data):
    # Calculate sum of squares within (SSW) and degrees of freedom within (dfw)
    ssw = sum(np.sum((group - np.mean(group)) ** 2) for group in data)
    # print([np.sqrt(np.sum((group - np.mean(group)) ** 2)) for group in data])
    dfw = sum(len(group) - 1 for group in data)

    # Calculate Mean Square Error (MSE)
    mse = ssw / dfw

    return mse


def perform_anova(data):
    # Perform ANOVA test
    f_statistic, p_value = f_oneway(*data)

    # Check the significance level
    alpha = 0.05
    if p_value < alpha:
        print(
            "Reject the null hypothesis: Significant differences between group means."
        )

        # Calculate MSE, and dfw
        mse = calculate_mse(data)
        n_per_group = len(data[0])

        # Extract Turkey's HSD values
        q_crit = studentized_range.ppf(1 - alpha, 12, 10 * 12 - 12)

        lsd = round(q_crit * np.sqrt(2 * mse / n_per_group), 2)
    else:
        lsd = "ns"
    return lsd
