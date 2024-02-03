from scipy.stats import f_oneway, t
import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import studentized_range


def ANOVA(data, se):
    # Perform ANOVA test
    f_statistic, p_value = f_oneway(*data)

    # Display the ANOVA results
    print("ANOVA F-statistic:", f_statistic)
    print("P-value:", p_value)

    # Check the significance level
    alpha = 0.05
    if p_value < alpha:
        print(
            "Reject the null hypothesis. There are significant differences between group means."
        )

        # Calculate MSE, and dfw
        n_per_group = 10  # len(data[0])
        n_groups = len(data)

        ssb = n_per_group / (n_groups - 1) * sum([se[i] ** 2 for i in range(n_groups)])
        sse = (
            (n_per_group - 1)
            / (n_per_group * (n_groups - 1))
            * sum([se[i] ** 2 for i in range(n_groups)])
        )

        ss = ssb + sse
        mse = ss / (n_per_group * n_groups - 1)

        # Calculate LSD
        q_crit = studentized_range.ppf(1 - alpha, 12, 10 * 12 - 12)

        lsd = round(q_crit * np.sqrt(2 * mse / n_per_group), 2)
    else:
        lsd = "ns"
    return lsd


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

    # Display the ANOVA results
    print("ANOVA F-statistic:", f_statistic)
    print("P-value:", p_value)

    # Check the significance level
    alpha = 0.05
    if p_value < alpha:
        print(
            "Reject the null hypothesis. There are significant differences between group means."
        )

        # Calculate MSE, and dfw
        mse = calculate_mse(data)
        n_per_group = len(data[0])

        # Calculate LSD

        # # Flatten the data for Tukey's HSD test
        # flattened_data = np.concatenate(data)

        # # Create labels for the groups
        # group_labels = np.repeat(
        #     np.arange(1, len(data) + 1), [len(group) for group in data]
        # )

        # # Perform Tukey's HSD test
        # tukey_result = pairwise_tukeyhsd(flattened_data, group_labels)

        # Extract HSD values
        q_crit = studentized_range.ppf(1 - alpha, 12, 10 * 12 - 12)
        # q = t.ppf(1 - alpha / 2, dfw)
        # print(q_crit / q)

        lsd = round(q_crit * np.sqrt(2 * mse / n_per_group), 2)
    else:
        lsd = "ns"
    return lsd


# # def testHSD():
# # Provided data
# data = [
#     [53.0, 66.0, 63.0, 66.0, 62.0, 66.0, 64.0, 59.0, 67.0, 57.0],
#     [59.0, 90.0, 66.0, 52.0, 82.0, 69.0, 70.0, 68.0, 70.0, 68.0],
#     [75.0, 80.0, 65.0, 67.0, 78.0, 66.0, 77.0, 78.0, 67.0, 77.0],
#     [69.0, 71.0, 59.0, 70.0, 56.0, 43.0, 70.0, 61.0, 63.0, 64.0],
#     [66.0, 71.0, 87.0, 54.0, 65.0, 66.0, 68.0, 59.0, 67.0, 66.0],
#     [78.0, 82.0, 76.0, 69.0, 72.0, 96.0, 79.0, 76.0, 77.0, 67.0],
#     [56.0, 53.0, 68.0, 57.0, 55.0, 68.0, 47.0, 56.0, 69.0, 51.0],
#     [69.0, 68.0, 65.0, 69.0, 60.0, 74.0, 69.0, 72.0, 65.0, 73.0],
#     [60.0, 70.0, 73.0, 68.0, 76.0, 81.0, 75.0, 77.0, 81.0, 77.0],
#     [63.0, 60.0, 55.0, 66.0, 54.0, 64.0, 48.0, 53.0, 59.0, 53.0],
#     [78.0, 68.0, 67.0, 78.0, 66.0, 66.0, 66.0, 52.0, 67.0, 71.0],
#     [79.0, 77.0, 75.0, 69.0, 73.0, 68.0, 63.0, 69.0, 57.0, 61.0],
# ]

# perform_anova(data)

# # Flatten the data for Tukey's HSD test
# flattened_data = np.concatenate(data)

# # Create labels for the groups
# group_labels = np.repeat(np.arange(1, len(data) + 1), [len(group) for group in data])

# # Perform Tukey's HSD test
# tukey_result = pairwise_tukeyhsd(flattened_data, group_labels)

# # Extract HSD values
# hsd_values = tukey_result.q_crit

# # Display the HSD values
# print("HSD values:\n", hsd_values)


def perform_anova2(data, se):
    # Perform ANOVA test
    f_statistic, p_value = f_oneway(*data)

    # Check the significance level
    alpha = 0.05
    if p_value < alpha:
        print(
            "Reject the null hypothesis: Significant differences between group means."
        )

        # Calculate MSE, and dfw
        sse = sum((se[i] ** 2 for i in range(len(se))))
        dfw = sum(len(group) - 1 for group in data)
        mse = sse / dfw
        print("MSE:", mse, end=" ")
        mse = calculate_mse(data)
        print(mse)
        n_per_group = len(data[0])

        # Extract HSD values
        q_crit = studentized_range.ppf(1 - alpha, 12, 10 * 12 - 12)

        # Calculate LSD
        lsd = round(q_crit * np.sqrt(2 * mse / n_per_group), 2)
    else:
        lsd = "ns"
    return lsd
