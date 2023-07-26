import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt

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


def csv_to_df(csv_in: str) -> pd.DataFrame:

    df = pd.read_csv(csv_in, index_col=[1])
    #print(df[''])

    return df

#Software Open Sourced?	Year Produced		Url

def chart_data(data_df: pd.DataFrame):
    slice_data_df = data_df[['Software Open Sourced?','Year Produced','Url']]
    slice_data_df.plot(kind="bar")
    plt.show()
    print(slice_data_df)
    num_rows = len(slice_data_df.index)
    print("xx", num_rows - slice_data_df['Software Open Sourced?'].value_counts())
    print("Total:", num_rows)
    print("Software Open Sourced? ", slice_data_df['Software Open Sourced?'].value_counts(), "No:")
    print("URL ", slice_data_df.count())



def main():

    df_responses = get_dataframe_from_csv('./data/responses.csv')


    # Get count of each http response code
    print(df_responses.groupby(1).count())

    df_all_data = csv_to_df("data/gtr_raw_data.csv")
    chart_data(df_all_data)

if __name__ == '__main__':
    main()