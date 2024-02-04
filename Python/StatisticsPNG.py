def lineChartMaxAvgMin(dataFrame, axes, xAxis, yAxis, xLabel, yLabel, xRange, yRange):
    axes.plot(
        dataFrame[xAxis],
        dataFrame[yAxis + "Max"],
        label="Max",
        marker="D",
        color="#4F83BC",
    )
    axes.plot(
        dataFrame[xAxis],
        dataFrame[yAxis + "Avg"],
        label="Average",
        marker="s",
        color="#BC5451",
    )
    axes.plot(
        dataFrame[xAxis],
        dataFrame[yAxis + "Min"],
        label="Min",
        marker="^",
        color="#8FB965",
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


import matplotlib.pyplot as plt


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
    plt.savefig(chartFileName, bbox_inches="tight")
