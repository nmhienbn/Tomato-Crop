import pandas as pd
import numpy as np
import ANOVA
import TreatmentName

excel_file_path = "resources/TomatoData.xlsx"
df = pd.read_excel(
    excel_file_path, sheet_name="Fruit morphology and quality", skiprows=3
)


def experimentCellsToNpArray(df):
    res = pd.DataFrame(columns=df.columns)
    res.insert(0, "Replication", "-")

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    # take all next cells
    def get_cell(row_index, column_name):
        values = []
        i = row_index
        while is_number(df.at[i, "No. plant"]):
            values.append(df.at[i, column_name])
            i += 1
        return ANOVA.calc_mean_sstot_size(values)

    def process_row(res: pd.DataFrame, index, row, treatmentName: list):
        newExperiment = pd.Series(index=res.columns)
        newExperiment["Replication"] = str(treatmentName[0])
        newExperiment["Treatment"] = treatmentName[1]
        for column, value in row.items():
            if column not in ["Replication", "Treatment", "No. plant"]:
                newExperiment[column] = get_cell(index, column)
        return res._append(newExperiment, ignore_index=True)

    def process_table(df: pd.DataFrame, res: pd.DataFrame):
        for index, row in df.iterrows():
            treatment = row["Treatment"]
            if TreatmentName.check(treatment):
                treatmentName = TreatmentName.standard(treatment)
                res = process_row(res, index, row, treatmentName)
        return res

    res = process_table(df, res)
    res.dropna(axis=1, how="all", inplace=True)
    return res


def groupSameTreatment(df):
    res = pd.DataFrame(
        columns=[
            "Treatment",
            "Fruit shape index (I=H/D)",
            "Number of locule",
            "Pericarp thickness",
            "Number of seed/fruit",
            "Brix",
        ]
    )
    return ANOVA.ANOVA_test_summary_table(df, res, "Treatment", MSEprecision=2)


res = experimentCellsToNpArray(df)
res = groupSameTreatment(res)
