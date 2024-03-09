import numpy as np
import scipy.stats as stats


def descriptive_stats(data: list, confidence_level=0.05):
    mean = np.mean(data)
    std_err = stats.sem(data)
    median = np.median(data)
    mode = stats.mode(data)[0]
    std_dev = np.std(data, ddof=1)
    sample_var = np.var(data, ddof=1)
    kurtosis = stats.kurtosis(data, bias=False)
    skewness = stats.skew(data, bias=False)
    data_range = np.ptp(data)
    minimum = np.min(data)
    maximum = np.max(data)
    summation = np.sum(data)
    count = len(data)
    confidence_interval_length = (
        stats.t.ppf(1 - confidence_level / 2, count - 1) * std_err
    )
    return [
        mean,
        std_err,
        median,
        mode,
        std_dev,
        sample_var,
        kurtosis,
        skewness,
        data_range,
        minimum,
        maximum,
        summation,
        count,
        confidence_interval_length,
    ]


def calculate_mse(data):
    # Calculate sum of squares within (SSW) and degrees of freedom within (dfw)
    ssw = sum(np.sum((group - np.mean(group)) ** 2) for group in data)
    dfw = sum(len(group) - 1 for group in data)

    # Calculate Mean Square Error (MSE)
    mse = ssw / dfw

    return mse


# calc mean, sstot, size from groups
def summary_data(groups_mean: list, groups_ssw: float, groups_size: list):
    mean = sum([mean * size for mean, size in zip(groups_mean, groups_size)]) / sum(
        groups_size
    )
    ssb = sum([(x - mean) ** 2 * size for x, size in zip(groups_mean, groups_size)])
    sstot = groups_ssw + ssb
    return mean, sstot, sum(groups_size)
