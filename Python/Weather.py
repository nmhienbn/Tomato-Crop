import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

excel_file_path = "resources/TomatoData.xlsx"
df = pd.read_excel(excel_file_path, sheet_name="Figure 1_Environmental data")


def standardizeData(df):
    columns_to_keep = (
        ["Year", "Month", "Day"]
        + list(
            df.columns[
                df.columns.get_loc("Temperature (° C)") : df.columns.get_loc(
                    "Temperature (° C)"
                )
                + 3
            ]
        )
        + list(
            df.columns[
                df.columns.get_loc("Humidity (%)") : df.columns.get_loc("Humidity (%)")
                + 3
            ]
        )
    )

    df = df[columns_to_keep]
    df = df.rename(
        columns={
            df.columns[3]: "°C Max",
            df.columns[4]: "°C Avg",
            df.columns[5]: "°C Min",
            df.columns[6]: "RH Max",
            df.columns[7]: "RH Avg",
            df.columns[8]: "RH Min",
        }
    )
    df.drop(0, axis=0, inplace=True)
    return df


df = standardizeData(df)


def calculateMeans(df):
    # Seeds were sown on nursery beds inside a net house on 15 October 2019.
    # The 30-day old seedlings were transplanted to the experimental open field.
    # Hence, 24 Oct 2019 (24th day) is the first day after transplanting (1st week).
    df["Weeknum"] = (df.index - 17) // 7
    res = pd.DataFrame()
    res["Weeknum"] = df["Weeknum"].unique()
    for i in range(3, 9):
        res[df.columns[i]] = df.groupby("Weeknum")[df.columns[i]].mean()
    return res


res = calculateMeans(df)
print(res)

# Plot line charts for each column
res_after_transplanting = res[(res["Weeknum"] >= 1) & (res["Weeknum"] <= 13)]
fig, axes = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"wspace": 0.5})


def configChart(axes, dataType, yLabel, xRange, yRange):
    axes.plot(
        res_after_transplanting["Weeknum"],
        res_after_transplanting[dataType + "Max"],
        label="Max",
        marker="D",
        color="#4F83BC",
    )
    axes.plot(
        res_after_transplanting["Weeknum"],
        res_after_transplanting[dataType + "Avg"],
        label="Average",
        marker="s",
        color="#BC5451",
    )
    axes.plot(
        res_after_transplanting["Weeknum"],
        res_after_transplanting[dataType + "Min"],
        label="Min",
        marker="^",
        color="#8FB965",
    )

    # Set chart title and axes labels
    axes.set_xlabel("Weeks after Transplanting")
    axes.set_ylabel(yLabel)
    # Add legend
    axes.legend()
    # Set axis limits
    axes.set_yticks(xRange)
    axes.set_xticks(yRange)
    axes.grid(axis="y")


configChart(
    axes[0], "°C ", "Temperature (° C)", np.arange(5, 31, 5), np.arange(1, 14, 1)
)
configChart(axes[1], "RH ", "Humidity (%)", np.arange(20, 101, 20), np.arange(1, 14, 1))
# Adjust layout to prevent clipping of titles
plt.tight_layout()
# Display the plots
# plt.show()

chartDir = "outputs/Figure1_Weather_Data.png"

# Save the chart as a PNG file
plt.savefig(chartDir)

# Open the saved PNG file using the default image viewer
os.system("start " + chartDir)
