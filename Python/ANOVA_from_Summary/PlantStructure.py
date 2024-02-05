import pandas as pd
import numpy as np
import ANOVA
import TukeyHSD
import TreatmentName

excel_file_path = "resources/TomatoData.xlsx"
tableDir = "outputs/Table1_Plant_structure_and_Fruit_set.png"
df = pd.read_excel(excel_file_path, sheet_name="Plant structure and fruit set")


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

    # Loop through all rows
    for index, row in df.iterrows():
        treatment = row["Treatment"]
        if TreatmentName.check(treatment):
            treatmentName = TreatmentName.standard(treatment)

            # average of next cells
            def get_cell(row_index, column_name):
                values = []
                i = row_index
                while i == row_index or pd.isna(df.at[i, "Treatment"]):
                    values.append(df.at[i, column_name])
                    i += 1
                return ANOVA.calc_mean_sstot_size(values)

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
            newExperiment["Fruit set"] = ANOVA.calc_mean_sstot_size(fruit_set)

            res = res._append(newExperiment, ignore_index=True)

    return res


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
    LSD["Treatment"] = "LSD" + TukeyHSD.get_subscript("(0.05)")

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

                se = ANOVA.stdError(means)
                res.at[index, column] = str(round(mean, 2)) + " ± " + str(round(se, 1))

            LSD[column], charGroup = ANOVA.perform_anova(
                groups_mean, groups_ssw, groups_size
            )
            for index, value in series.items():
                res.at[index, column] += TukeyHSD.get_superscript(charGroup[index])
    res = res._append(LSD, ignore_index=True)
    return res


# Open the saved PNG image
import os
import StatisticsPNG as SPNG

columns_to_remove = [2, 4, 6, 17, 18]
df = df.drop(df.columns[columns_to_remove], axis=1)
avg = experimentCellsToNpArray(df)
res = assessAllReplications(avg)

SPNG.configTable(res, tableDir)
os.system("start " + tableDir)