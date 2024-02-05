from scipy.stats import f, studentized_range, f_oneway
import numpy as np
import TukeyHSD
import pandas as pd


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


def perform_anova_summary(
    groups_mean: list, groups_ssw: float, groups_size: list, alpha=0.05
):
    # Perform ANOVA test
    mean, sstot, size = anova_table(groups_mean, groups_ssw, groups_size)
    n_groups = len(groups_mean)
    dfb = n_groups - 1
    dfw = size - n_groups
    ssb = sum([(x - mean) ** 2 * size for x, size in zip(groups_mean, groups_size)])
    ssw = sstot - ssb
    msw = ssw / dfw
    msb = ssb / dfb
    f_value = msb / msw
    p_value = f.sf(f_value, dfb, dfw)
    # print(mean, ssw, size, dfw, dfb, ssb, msw, msb, f_value, p_value)

    charGroup = [""] * n_groups
    # print(nGroups)
    # Check the significance level
    if p_value < alpha:
        # Reject the null hypothesis: Significant differences between group means.
        n_per_group = round(size / n_groups, 0)

        # Extract Turkey's HSD values
        q_crit = studentized_range.ppf(1 - alpha, n_groups, dfw)

        lsd = q_crit * np.sqrt(2 * msw / n_per_group)

        charGroup = TukeyHSD.getLabels(groups_mean, lsd)
        lsd = round(lsd, 2)
    else:
        lsd = "ns"
    return lsd, charGroup


def perform_anova(data, alpha=0.05):
    # Perform ANOVA test
    f_statistic, p_value = f_oneway(*data)

    charGroup = [""] * len(data)
    # Check the significance level
    if p_value < alpha:
        # Reject the null hypothesis: Significant differences between group means.

        # Calculate MSE, and dfw
        mse = calculate_mse(data)
        n_groups = len(data)
        n_per_group = len(data[0])

        # Extract Turkey's HSD values
        q_crit = studentized_range.ppf(
            1 - alpha, n_groups, n_groups * n_per_group - n_groups
        )

        # Turkey's HSD characteristic group
        groups_mean = [np.mean(group) for group in data]
        lsd = q_crit * np.sqrt(2 * mse / n_per_group)
        charGroup = TukeyHSD.getLabels(groups_mean, lsd)

        lsd = round(lsd, 2)
    else:
        # Accept the null hypothesis: "No significant" differences between group means.
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


def ANOVA_test_summary_table(
    df: pd.DataFrame,
    summaryDf: pd.DataFrame,
    groupCol: str,
    needMSE=False,
    ANOVAtest=True,
    alpha=0.05,
):
    summaryDf[groupCol] = df[groupCol].unique()
    LSD = pd.Series(index=summaryDf.columns)
    LSD[groupCol] = "LSD" + TukeyHSD.get_subscript("(0.05)")

    nrows = len(summaryDf[groupCol])

    for column, series in summaryDf.items():
        if column != groupCol:
            groups_mean = []
            groups_ssw = 0
            groups_size = []
            for index in range(nrows):
                colVal = summaryDf.at[index, groupCol]
                vals = df[df[groupCol] == colVal][column].tolist()

                means, ssws, sizes = zip(
                    *[(mean, ssw, size) for mean, ssw, size in vals if mean is not None]
                )
                mean, ssw, size = anova_table(means, sum(ssws), sizes)
                mse = stdError(means)

                if needMSE:
                    summaryDf.at[index, column] = (
                        str(round(mean, 2)) + " ± " + str(round(mse, 1))
                    )
                elif ANOVAtest:
                    summaryDf.at[index, column] = str(round(mean, 2))
                else:
                    summaryDf.at[index, column] = [mean, mse]

                groups_mean.append(mean)
                groups_ssw += ssw
                groups_size.append(size)

            if ANOVAtest:
                LSD[column], charGroup = perform_anova_summary(
                    groups_mean, groups_ssw, groups_size, alpha=alpha
                )
                for index, value in series.items():
                    summaryDf.at[index, column] += TukeyHSD.get_superscript(
                        charGroup[index]
                    )
    if ANOVAtest:
        summaryDf = summaryDf._append(LSD, ignore_index=True)
    return summaryDf
