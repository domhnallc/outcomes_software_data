import pandas as pd

"""Helper functions"""


def get_dataframe_from_csv(
    file: str,
) -> pd.DataFrame:
    df_all_data = pd.read_csv(file, header=None)

    return df_all_data


def filter_dataframe(df_in: pd.DataFrame, columns: list) -> pd.DataFrame:
    filtered_df = df_in[columns]
    return filtered_df


def csv_to_df(csv_in: str, index_col: str, header: int) -> pd.DataFrame:
    df = pd.read_csv(csv_in, index_col=index_col, header=0, encoding="utf-8-sig")

    return df


def count_per_funder(df_in: pd.DataFrame):
    vals = (
        df_in.groupby("Funding OrgName", sort=True).size().sort_values(ascending=False)
    )

    return vals


def count_per_PI(df_in: pd.DataFrame):
    vals = df_in.groupby("PIId", sort=True).size().sort_values(ascending=False)

    return vals


def count_per_RO(df_in: pd.DataFrame):
    vals = df_in.groupby("LeadRO Name", sort=True).size().sort_values(ascending=False)

    return vals


def count_per_open_sourced(df_in: pd.DataFrame):
    vals = (
        df_in.groupby("Software Open Sourced?", sort=True)
        .size()
        .sort_values(ascending=False)
    )
    return vals


def count_per_year(df_in: pd.DataFrame):
    df_in["Year Produced"] = df_in["Year Produced"].fillna("Missing")
    vals = df_in.groupby("Year Produced", sort=True).size()

    return vals


def count_per_department(df_in: pd.DataFrame):
    vals = df_in.groupby("Department", sort=True).size().sort_values(ascending=False)

    return vals


def print_out(title: str, df_in: pd.DataFrame):
    print("\n\n", title, "\n\n")
    print(df_in.describe())
    print(df_in)
