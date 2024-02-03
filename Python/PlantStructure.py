import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ANOVA

excel_file_path = "resources/TomatoData.xlsx"
tableDir = "outputs/Table1_Plant_structure_and_Fruit_set.png"
df = pd.read_excel(excel_file_path, sheet_name="Plant structure and fruit set")


def stdError(values):
    return np.std(values, ddof=1) / np.sqrt(len(values))


# mean, ssw, size
def calc_mean_mse(data):
    data = np.array(data)
    mean = data.mean()
    return [mean, sum((val - mean) ** 2 for val in data), len(data)]


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

            # average of next cells
            def get_cell(row_index, column_name):
                values = []
                i = row_index
                while i == row_index or pd.isna(df.at[i, "Treatment"]):
                    values.append(df.at[i, column_name])
                    i += 1
                return calc_mean_mse(values)

            newExperiment = pd.Series(index=res.columns)
            newExperiment["Replication"] = str(treatmentName[0])
            newExperiment["Treatment"] = treatmentName[1]
            for column, value in row.items():
                if (
                    column != "Replication"
                    and column != "Treatment"
                    and column != "Fruit set"
                ):
                    newExperiment[column] = get_cell(index, column)

            fruit_set = []
            for i in range(1, 6):
                col = "Fruit set " + str(i)
                mean = newExperiment[col][0]
                if np.isnan(mean) != True:
                    fruit_set.append(mean * 100)
            newExperiment["Fruit set"] = calc_mean_mse(fruit_set)

            res = res._append(newExperiment, ignore_index=True)

    return res


# function to convert to superscript
def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans("".join(normal), "".join(super_s))
    return x.translate(res)


def get_sub(x):
    normal = "0123456789+-=()."
    sub_s = "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎."
    res = x.maketrans("".join(normal), "".join(sub_s))
    return x.translate(res)


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
    LSD["Treatment"] = "LSD" + get_sub("(0.05)")

    nrows = len(res["Treatment"])

    for column, series in res.items():
        if column != "Treatment":
            groups_mean = []
            groups_ssw = 0
            groups_size = []
            for index in range(nrows):
                treatment = res.at[index, "Treatment"]
                filtered_values = avg[avg["Treatment"] == treatment]

                vals = filtered_values[column].tolist()
                means = []
                ssws = 0
                sizes = []

                for mean, ssw, size in vals:
                    if mean is not None:
                        means.append(mean)
                        ssws += ssw
                        sizes.append(size)

                mean, ssw, size = ANOVA.anova_table(means, ssws, sizes)

                groups_mean.append(mean)
                groups_ssw += ssw
                groups_size.append(size)

                se = stdError(means)
                res.at[index, column] = str(round(mean, 2)) + " ± " + str(round(se, 1))

            LSD[column], charGroup = ANOVA.perform_anova(
                groups_mean, groups_ssw, groups_size
            )
            for index, value in series.items():
                res.at[index, column] += get_super(charGroup[index])
    res = res._append(LSD, ignore_index=True)
    return res


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

columns_to_remove = [2, 4, 6, 17, 18]
df = df.drop(df.columns[columns_to_remove], axis=1)
avg = experimentCellsToNpArray(df)
res = assessAllReplications(avg)

configChart(res, tableDir)
os.system("start " + tableDir)
