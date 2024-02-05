from scipy.stats import f, studentized_range
import numpy as np
import TukeyHSD


def calculate_mse(data):
    # Calculate sum of squares within (SSW) and degrees of freedom within (dfw)
    ssw = sum(np.sum((group - np.mean(group)) ** 2) for group in data)
    dfw = sum(len(group) - 1 for group in data)

    # Calculate Mean Square Error (MSE)
    mse = ssw / dfw

    return mse


def stdError(values):
    return np.std(values, ddof=1) / np.sqrt(len(values))


# mean, ssw, size from data
def calc_mean_sstot_size(data: list):
    data = np.array(data)
    mean = data.mean()
    return [mean, sum((val - mean) ** 2 for val in data), len(data)]


def perform_anova(groups_mean: list, groups_ssw: float, groups_size: list, alpha=0.05):
    # Perform ANOVA test
    mean, sstot, size = anova_table(groups_mean, groups_ssw, groups_size)
    nGroups = len(groups_mean)
    dfb = nGroups - 1
    dfw = size - nGroups
    ssb = sum([(x - mean) ** 2 * size for x, size in zip(groups_mean, groups_size)])
    ssw = sstot - ssb
    msw = ssw / dfw
    msb = ssb / dfb
    f_value = msb / msw
    p_value = f.sf(f_value, dfb, dfw)
    # print(mean, ssw, size, dfw, dfb, ssb, msw, msb, f_value, p_value)

    charGroup = [""] * nGroups
    # print(nGroups)
    # Check the significance level
    if p_value < alpha:
        # Reject the null hypothesis: Significant differences between group means.

        # Extract Turkey's HSD values
        q_crit = studentized_range.ppf(1 - alpha, 12, 10 * 12 - 12)

        n_per_group = size / nGroups
        lsd = q_crit * np.sqrt(2 * msw / n_per_group)

        charGroup = TukeyHSD.getLabels(groups_mean, lsd)
        lsd = round(lsd, 2)
    else:
        lsd = "ns"
    return lsd, charGroup


# calc mean, sstot, size from groups
def anova_table(groups_mean: list, groups_ssw: float, groups_size: list):
    mean = sum([mean * size for mean, size in zip(groups_mean, groups_size)]) / sum(
        groups_size
    )
    ssb = sum([(x - mean) ** 2 * size for x, size in zip(groups_mean, groups_size)])
    sstot = groups_ssw + ssb
    return mean, sstot, sum(groups_size)
