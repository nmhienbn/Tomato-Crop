import pandas as pd
import numpy as np
import ANOVA
import TukeyHSD
import TreatmentName

excel_file_path = "resources/TomatoData.xlsx"
tableDir = "outputs/Table1_Plant_structure_and_Fruit_set.png"
df = pd.read_excel(excel_file_path, sheet_name="Plant structure and fruit set")


def remove_useless_columns(df):
    columns_to_remove = [2, 4, 6, 17, 18]
    df = df.drop(df.columns[columns_to_remove], axis=1)
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
    return df


def experimentCellsToNpArray(df):
    res = pd.DataFrame(columns=df.columns)
    res.insert(0, "Replication", "-")

    # take all next cells
    def get_cell(row_index, column_name):
        values = []
        i = row_index
        while i == row_index or pd.isna(df.at[i, "Treatment"]):
            values.append(df.at[i, column_name])
            i += 1
        return ANOVA.calc_mean_sstot_size(values)

    def process_row(res: pd.DataFrame, index, row, treatmentName: list):
        newExperiment = pd.Series(index=res.columns)
        newExperiment["Replication"] = str(treatmentName[0])
        newExperiment["Treatment"] = treatmentName[1]
        for column, value in row.items():
            if column not in ["Replication", "Treatment"]:
                newExperiment[column] = get_cell(index, column)
        return res._append(newExperiment, ignore_index=True)

    def process_table(df: pd.DataFrame, res: pd.DataFrame):
        for index, row in df.iterrows():
            treatment = row["Treatment"]
            if TreatmentName.check(treatment):
                treatmentName = TreatmentName.standard(treatment)
                res = process_row(res, index, row, treatmentName)
        return res

    def calc_fruit_set(res):
        for index, row in res.iterrows():
            fruit_set = []
            for i in range(1, 6):
                col = "Fruit set " + str(i)
                if np.isnan(row[col][0]) != True:
                    fruit_set.append(row[col][0] * 100)
            res.at[index, "Fruit set"] = ANOVA.calc_mean_sstot_size(fruit_set)
        return res

    res = process_table(df, res)
    res["Fruit set"] = ""
    res = calc_fruit_set(res)
    return res


def groupSameTreatment(df):
    res = pd.DataFrame(
        columns=[
            "Treatment",
            "First truss\nheight",
            "Last truss\nheight",
            "Number of\nleaf/plant",
            "Fruit set",
        ]
    )
    return ANOVA.ANOVA_test_summary_table(df, res, "Treatment", needMSE=True)


# Open the saved PNG image
import os
import StatisticsPNG as SPNG

df = remove_useless_columns(df)
res = experimentCellsToNpArray(df)
res = groupSameTreatment(res)

SPNG.configTable(res, tableDir)
os.system("start " + tableDir)
