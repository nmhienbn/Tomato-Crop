import statsData as sd
import pandas as pd


def print_table(date_name: str, index_name: str):
    date_name, index_name, res = sd.get_data(date_name, index_name)
    export_csv = "outputs/Số liệu " + index_name + " ngày " + date_name + ".csv"
    try:
        res.to_csv(export_csv, sep=",", index=False)
        print("File exported to: " + export_csv)
    except:
        print("Error exporting file: " + export_csv)


def print_statistic(date_name, index_name):
    index_name, date_name, res, anova = sd.statistic(date_name, index_name)
    export_csv = "outputs/Thống kê " + index_name + " ngày " + date_name + ".csv"

    # Insert an empty column filled with NaN values between dataframes
    empty_col = pd.DataFrame({"": [float("nan")]})

    # Concatenate dataframes along columns with empty column between them
    combined_df = pd.concat([res, empty_col, anova], axis=1)

    try:
        combined_df.to_csv(export_csv, sep=",", index=False)
        print("File exported to: " + export_csv)
    except:
        print("Error exporting file: " + export_csv)


def print_box_plot(date_name, index_name, y_start, y_stop, y_step):
    sd.box_plot(date_name, index_name, y_start, y_stop, y_step)


def print_anova_each_iteration(date_name, index_name):
    res = sd.anova_each_iteration(date_name, index_name)
    export_csv = "outputs/ANOVA test " + index_name + " ngày " + date_name + ".csv"
    try:
        res.to_csv(export_csv, sep=",", index=False, header=False)
        print("File exported to: " + export_csv)
    except:
        print("Error exporting file: " + export_csv)


# # 2.1
# print_table("19-10-2023", "chỉ tiêu chùm ")
# print_table("26-10-2023", "chỉ tiêu chùm ")
# print_table("09-11-2023", "chỉ tiêu chùm ")

# # 2.2
# print_table("05-10-2023", "Chỉ tiêu diệp lục ")
# print_table("19-10-2023", "Chỉ tiêu diệp lục ")
# print_table("26-10-2023", "Chỉ tiêu diệp lục ")
# print_table("09-11-2023", "Chỉ tiêu diệp lục ")

# # 3.1.A
# print_statistic("09-11-2023", "chỉ tiêu chùm ")
# print_box_plot("09-11-2023", "chỉ tiêu chùm ", 0, 18, 2)

# # 3.1.B
# print_statistic("26-10-2023", "Chỉ tiêu diệp lục ")
# print_box_plot("26-10-2023", "Chỉ tiêu diệp lục ", 0, 70, 10)

# 3.2.A
print_anova_each_iteration("19-10-2023", "chỉ tiêu chùm ")

# 3.2.B
print_anova_each_iteration("19-10-2023", "Chỉ tiêu diệp lục ")
