import pandas as pd

'''Helper functions'''

def get_dataframe_from_csv(file: str,) -> pd.DataFrame:
    df_all_data = pd.read_csv(file, header=None)

    return df_all_data


def filter_dataframe(df_in: pd.DataFrame) -> pd.DataFrame:
    filtered_df = df_in[
        [
        ]
    ]
    return filtered_df


def main():

    df_all_data = get_dataframe_from_csv('./data/responses.csv')


    # Get count of each http response code
    print(df_all_data.groupby(1).count())

if __name__ == '__main__':
    main()