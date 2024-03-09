import datetime
import pandas as pd
import numpy as np

excel_file_path = "resources/dataset.xlsx"
df = pd.read_excel(excel_file_path, sheet_name="Bảng tổng hợp ")
date_col = "Ngày thu mẫu"
formula_col = "Tên công thức"
block_col = "Block"

formulas = df[formula_col].dropna().astype(str).apply(lambda x: x.strip()).unique()
df[formula_col] = df[formula_col].astype(str).apply(lambda x: x.strip())
# print(formulas)


def format_datetime(value):
    if isinstance(value, datetime.datetime):
        return value.strftime("%m-%d-%Y")
    elif isinstance(value, str):
        return value.replace("/", "-")
    else:
        return value


df[date_col] = df[date_col].apply(format_datetime)
dates = df[date_col].dropna().unique()
print(np.array(dates))


def data_from(date_name, formula_name, index_name, dropna=True):
    res = df[(df[date_col] == date_name) & (df[formula_col] == formula_name)][
        index_name
    ]
    if dropna:
        res = res.dropna()
    return res.to_list()


def print_table(table_name: str, data: pd.DataFrame):
    print("-" * 100)
    print(table_name)
    print(data.to_string(index=False))
    print("-" * 100)
