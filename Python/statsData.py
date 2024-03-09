import datetime
import numpy as np
import pandas as pd
import ANOVA
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import getData

formulas = getData.formulas
df = getData.df
date_col = getData.date_col
formula_col = getData.formula_col
block_col = getData.block_col


def get_data(date_name: str, index_name: str):
    block = df[(df[date_col] == date_name) & (df[formula_col] == formulas[0])][
        block_col
    ].astype(int)
    prev = None  # Use None instead of np.nan for comparison with integers
    for i in range(len(block)):
        if block.iloc[i] == prev:
            block.iat[i] = ""
        else:
            prev = block.iloc[i]

    res = pd.DataFrame()
    res["Block"] = block
    for formula_name in formulas:
        res[formula_name] = getData.data_from(
            date_name, formula_name, index_name, dropna=False
        )
    return date_name, index_name, res


def statistic(date_name, index_name):
    datas = []
    res = pd.DataFrame(
        {
            "Statistic": [
                "Mean",
                "Standard Error",
                "Median",
                "Mode",
                "Standard Deviation",
                "Sample Variance",
                "Kurtosis",
                "Skewness",
                "Range",
                "Minimum",
                "Maximum",
                "Sum",
                "Count",
                "Confidence Interval Length",
            ],
        }
    )
    for formula_name in getData.formulas:
        data = getData.data_from(date_name, formula_name, index_name)
        res[formula_name] = statistics.descriptive_stats(data)
        datas.append(data)
    if isinstance(date_name, datetime.datetime):
        date_name = date_name.strftime("%Y\\%m\\%d")
    return index_name, date_name, res, ANOVA.anova_summary_table(datas)


def box_plot(date_name, index_name, y_start, y_stop, y_step):
    datas = []
    for formula_name in formulas:
        data = getData.data_from(date_name, formula_name, index_name)
        datas.append(data)
    print(datas)
    plt.figure(figsize=(8, 6))
    plt.grid(True)
    ax = sns.boxplot(
        datas,
        showmeans=True,
        meanprops={
            "marker": "x",
            "markeredgecolor": "black",
        },
        whis=1.5,
    )
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)

    y_ticks = np.arange(y_start, y_stop + y_step, y_step)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks)

    plt.title("Box Plot")
    plt.xlabel("Data")
    plt.ylabel("Values")
    output_file = "outputs/Thống kê về " + index_name + " " + date_name
    print(output_file)
    plt.savefig(output_file, dpi=300)


def anova_each_iteration(date_name, index_name):
    res_df = []
    for formula_name in formulas:
        datas = []
        fdatas = []
        data = df[(df[date_col] == date_name) & (df[formula_col] == formula_name)]
        iterations = data["Block"].dropna().unique()
        for iteration in iterations:
            tmp = data[(data["Block"] == iteration)][index_name].dropna().to_list()
            datas.append(tmp)
            fdatas.append([iteration.astype(int)] + tmp)

        length = max(max(len(fdata) for fdata in fdatas), 2)
        fdatas = [fdata + [np.nan] * (length - len(fdata)) for fdata in fdatas]

        formula = [formula_name] + [np.nan] * (length - 1)
        pvalues = ["P-value", ANOVA.anova_summary_table(datas).loc[0, "P-value"]] + [
            np.nan
        ] * (length - 2)
        fdatas = [formula] + fdatas + [pvalues]

        res_df.append(pd.DataFrame(fdatas).transpose())
        res_df.append(pd.DataFrame([[np.nan]]))
    return pd.concat(res_df, axis=0)
