from scipy.stats import f, f_oneway, studentized_range
import numpy as np
import pandas as pd
import statistics
import TukeyHSD


def anova_summary_table(data, alpha=0.05):
    tmp = [x for y in data for x in y]
    means = np.mean(tmp)

    # Sum of squares
    ssw = sum(np.sum((group - np.mean(group)) ** 2) for group in data)
    ssb = sum(((np.mean(group) - means) ** 2) * len(group) for group in data)
    sstot = ssw + ssb

    # Degrees of freedom
    dfw = sum(len(group) - 1 for group in data)
    dfb = len(data) - 1
    dftot = dfw + dfb

    # Mean Square
    msw = ssw / dfw
    msb = ssb / dfb

    # Perform ANOVA test
    f_statistic, p_value = f_oneway(*data)
    f_critical = f.ppf(1 - alpha, dfb, dfw)

    # Creating DataFrame
    df = pd.DataFrame(
        {
            "Source": ["Group", "Error", "Total"],
            "SS": [ssb, ssw, sstot],
            "df": [dfb, dfw, dftot],
            "MS": [msb, msw, ""],
            "F": [f_statistic, "", ""],
            "P-value": [p_value, "", ""],
            "F-critical": [f_critical, "", ""],
        }
    )
    return df


def anova_from_summary_data(
    groups_mean: list, groups_ssw: float, groups_size: list, alpha=0.05
):
    # Perform ANOVA test
    mean, sstot, size = statistics.summary_data(groups_mean, groups_ssw, groups_size)
    n_groups = len(groups_mean)

    # Degrees of freedom
    dfb = n_groups - 1
    dfw = size - n_groups

    # Sum of squares
    ssb = sum([(x - mean) ** 2 * size for x, size in zip(groups_mean, groups_size)])
    ssw = sstot - ssb

    # Mean Square
    msw = ssw / dfw
    msb = ssb / dfb

    # Perform ANOVA test
    f_value = msb / msw
    p_value = f.sf(f_value, dfb, dfw)

    charGroup = [""] * n_groups

    # Check the significance level
    if p_value < alpha:
        # Reject the null hypothesis: Significant differences between group means.
        n_per_group = round(size / n_groups, 0)

        # Extract Turkey's HSD values
        q_crit = studentized_range.ppf(1 - alpha, n_groups, dfw)

        lsd = q_crit * np.sqrt(2 * msw / n_per_group)

        charGroup = TukeyHSD.getLabels(groups_mean, groups_size, q_crit, msw)
        lsd = round(lsd, 2)
    else:
        lsd = "ns"
    return lsd, charGroup


def ANOVA_table_Tukey_HSD(data, alpha=0.05):
    df = anova_summary_table(data, alpha)
    p_value = df.loc[0, "P-value"]
    msw = df.loc[1, "MS"]
    dfw = df.loc[1, "df"]
    n_groups = len(data)
    charGroup = [""] * n_groups

    # Check the significance level
    if p_value < alpha:
        # Reject the null hypothesis: Significant differences between group means.
        # Extract Turkey's HSD values
        q_crit = studentized_range.ppf(1 - alpha, n_groups, dfw)
        groups_mean = [np.mean(group) for group in data]
        groups_size = [len(group) for group in data]
        charGroup = TukeyHSD.getLabels(groups_mean, groups_size, q_crit, msw)
    return df, charGroup
