import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter


def lineChartMaxAvgMin(dataFrame, axes, xAxis, yAxis, xLabel, yLabel, xRange, yRange):
    markers = ["D", "s", "^"]
    colors = ["#4F83BC", "#BC5451", "#8FB965"]
    labels = ["Max", "Avg", "Min"]

    for marker, color, label in zip(markers, colors, labels):
        axes.plot(
            dataFrame[xAxis],
            dataFrame[f"{yAxis}{label}"],
            label=label,
            marker=marker,
            color=color,
        )

    # Set chart title and axes labels
    axes.set_xlabel(xLabel)
    axes.set_ylabel(yLabel)
    # Add legend
    axes.legend()
    # Set axis limits
    axes.set_yticks(xRange)
    axes.set_xticks(yRange)
    axes.grid(axis="y")


def colChart(
    df: pd.DataFrame,
    columns_to_plot: list,
    x_col: list,
    x_label: str,
    y_label: str,
    chart_file_name: str,
):
    # Extract values and errors separately for each column
    values = [[x[0] for x in val] for val in df[columns_to_plot].values]
    errors = [[x[1] for x in val] for val in df[columns_to_plot].values]

    # Specify custom colors for each column
    colors = ["#4F83BC", "#BC5451", "#8FB965"]

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set the width of the bars
    bar_width = 0.2

    # Calculate the x-coordinates for each group of bars
    x_positions = np.arange(len(df))

    # Plotting the grouped bar chart without error bars
    for i, col in enumerate(columns_to_plot):
        ax.bar(
            x_positions + i * bar_width,
            [v[i] for v in values],
            width=bar_width,
            color=colors[i],
            label=col,
            zorder=2,
        )

    # Plotting the error bars
    for i, col in enumerate(columns_to_plot):
        ax.errorbar(
            x_positions + i * bar_width,
            [v[i] for v in values],
            yerr=[e[i] for e in errors],
            fmt="none",
            capsize=3,
            color="black",
            zorder=1,
        )

    # Set chart title and axes labels
    ax.set_title(f'Column Chart of Columns {", ".join(columns_to_plot)}')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Set x-axis tick labels and rotation
    ax.set_xticks(x_positions + (len(columns_to_plot) - 1) * bar_width / 2)
    ax.set_xticklabels(x_col, ha="right")

    # Set y-axis ticks and format labels
    ax.set_yticks(range(0, 141, 20))
    formatter = FuncFormatter(lambda y, _: f"{y:.3f}")
    ax.yaxis.set_major_formatter(formatter)

    # Add grid lines on the y-axis
    ax.grid(axis="y")

    # Add legend
    ax.legend()

    # Save the chart to the specified file
    plt.savefig(chart_file_name, bbox_inches="tight", dpi=300)


def configTable(dataFrame, chartFileName):
    fig, ax = plt.subplots(figsize=(5, 5), dpi=300)
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(
        cellText=dataFrame.values,
        colLabels=dataFrame.columns,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6)
    table.auto_set_column_width(
        [i for i in range(len(dataFrame.columns))]
    )  # Specify the indices of columns to adjust
    for cell in table._cells:
        if cell[0] == 0:  # Check if it's the first row
            cell_obj = table._cells[cell]
            cell_obj.set_height(cell_obj.get_height() * 1.5)
    plt.savefig(chartFileName, bbox_inches="tight", dpi=300)
