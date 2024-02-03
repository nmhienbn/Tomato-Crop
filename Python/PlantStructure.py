import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ANOVA

excel_file_path = "resources/TomatoData.xlsx"
df = pd.read_excel(excel_file_path, sheet_name="Plant structure and fruit set")
meanTables = pd.DataFrame()

columns_to_remove = [2, 4, 6, 17, 18]
df = df.drop(df.columns[columns_to_remove], axis=1)


def stdError(values):
    return np.std(values, ddof=1) / np.sqrt(len(values))


def experimentCellsToNpArray(df):
    df.columns = [
        "Treatment",
        "First truss\nheight",
        "Last truss\nheight",
        "Number of\nleaf/plant",
        "Number of\nflower 1",
        "Number of\nflower 2",
        "Number of\nflower 3",
        "Number of\nflower 4",
        "Number of\nflower 5",
        "Fruit set 1",
        "Fruit set 2",
        "Fruit set 3",
        "Fruit set 4",
        "Fruit set 5",
    ]
    res = pd.DataFrame(columns=df.columns)
    res.insert(0, "Replication", "-")
    res["Fruit set"] = "-"

    def isTreatmentName(treatment):
        if isinstance(treatment, str):
            code = treatment.split("-")
            return len(code) == 3 and int(code[1]) <= 4 and int(code[2]) <= 3
        else:
            return False

    def getTreatmentName(treatment):
        str = treatment.split("-")
        return [str[0], "S" + str[1] + "T" + str[2]]

    # Loop through all rows
    for index, row in df.iterrows():
        treatment = row["Treatment"]
        if isTreatmentName(treatment):
            treatmentName = getTreatmentName(treatment)

            # average of next 5 cells
            def calculate_avg_se(row_index, column_name):
                try:
                    values = df.iloc[row_index : row_index + 5][column_name].values
                    return values
                except IndexError:
                    return "-"

            newExperiment = pd.Series(index=res.columns)
            newExperiment["Replication"] = str(treatmentName[0])
            newExperiment["Treatment"] = treatmentName[1]
            for column, value in row.items():
                if (
                    column != "Replication"
                    and column != "Treatment"
                    and column != "Fruit set"
                ):
                    newExperiment[column] = calculate_avg_se(index, column)

            fruit_set = []
            for i in range(1, 6):
                col = "Fruit set " + str(i)
                mean = newExperiment[col].mean()
                if np.isnan(mean) != True:
                    fruit_set.append(mean * 100)
            newExperiment["Fruit set"] = np.array(fruit_set)

            res = res._append(newExperiment, ignore_index=True)

    return res


avg = experimentCellsToNpArray(df)


def assessAllReplications(avg):
    res = pd.DataFrame(
        columns=[
            "Treatment",
            "First truss\nheight",
            "Last truss\nheight",
            "Number of\nleaf/plant",
            "Fruit set",
        ]
    )
    LSD = pd.Series(index=res.columns)
    res["Treatment"] = avg["Treatment"].unique()
    LSD["Treatment"] = "LSD"
    ses = []

    for column, series in res.items():
        if column != "Treatment":
            group_data = []
            for index, value in series.items():
                treatment = res.at[index, "Treatment"]
                filtered_values = avg[avg["Treatment"] == treatment]

                vals = filtered_values[column].tolist()
                arr = []
                elements = []

                for x in vals:
                    if x is not None:
                        arr.append(x.mean())
                        elements.extend(x)

                arr = np.array(arr)
                mean = arr.mean()
                se = stdError(arr)
                group_data.append(elements)
                ses.append(se)

                res.at[index, column] = str(round(mean, 2)) + " ± " + str(round(se, 1))

            for x in group_data:
                print(stdError(x))
            print(column)
            LSD[column] = ANOVA.perform_anova(group_data)
    res = res._append(LSD, ignore_index=True)
    return res


res = assessAllReplications(avg)


def configChart(res, chartFileName):
    fig, ax = plt.subplots(figsize=(5, 5), dpi=300)
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(
        cellText=res.values,
        colLabels=res.columns,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6)
    table.auto_set_column_width([0, 1, 2])  # Specify the indices of columns to adjust
    for cell in table._cells:
        if cell[0] == 0:  # Check if it's the first row
            cell_obj = table._cells[cell]
            cell_obj.set_height(cell_obj.get_height() * 1.5)
    plt.savefig(chartFileName, bbox_inches="tight")


# Open the saved PNG image
import os

tableDir = "outputs/Table2_Plant_structure_and_Fruit_set.png"

configChart(res, tableDir)
os.system("start " + tableDir)