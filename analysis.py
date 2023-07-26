import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt


'''gtr_raw_data.csv headers:
Funding OrgName	
Project Reference	
ProjectCategory	
Outcome Type	
LeadRO Name	
Department	
PI Surname	
PI First Name	
PI Orcid iD	
Outcome Title	
Description	
Type of Technology	
Software Open Sourced?	
Year Produced	
Impact	
Url	
GTR OutcomeId	
GTR Outcome URL	
GTRProjectUrl	
ProjectId	
FundingOrgId	
LeadROId	
PIId
'''

'''Helper functions'''

def get_dataframe_from_csv(file: str,) -> pd.DataFrame:
    df_all_data = pd.read_csv(file, header=None)

    return df_all_data


def filter_dataframe(df_in: pd.DataFrame, columns: list) -> pd.DataFrame:
    filtered_df = df_in[columns]
    return filtered_df


def csv_to_df(csv_in: str, index_col: str, header: int) -> pd.DataFrame:

    df = pd.read_csv(csv_in, index_col=index_col, header=0, encoding='utf-8-sig')
    
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

def count_per_RO(df_in: pd.DataFrame):
    ''' Count entries of sware per research organisation'''

def count_per_funder(df_in: pd.DataFrame):
    print("Counts per research funder \n\n")
    print(df_in.describe())
    print(df_in)
   
    #df_in.groupby('Funding OrgName').count()
    vals = df_in.groupby('Funding OrgName', sort=True).size().sort_values(ascending=False)
    print(vals)

def count_per_PI(df_in: pd.DataFrame):
    print("Counts per PI \n\n")
    print(df_in.describe())
    print(df_in)
   
    #df_in.groupby('Funding OrgName').count()
    vals = df_in.groupby('PIId', sort=True).size().sort_values(ascending=False)
    print(vals)

def count_per_RO(df_in: pd.DataFrame):
    print("Counts per RO \n\n")
    print(df_in.describe())
    print(df_in)
   
    #df_in.groupby('Funding OrgName').count()
    vals = df_in.groupby('LeadRO Name', sort=True).size().sort_values(ascending=False)
    print(vals)

def count_per_open_sourced(df_in: pd.DataFrame):
    print("Counts per open sourced \n\n")
    print(df_in.describe())
    print(df_in)
   
    #df_in.groupby('Funding OrgName').count()
    vals = df_in.groupby('Software Open Sourced?', sort=True).size().sort_values(ascending=False)
    print(vals)	


def count_per_year(df_in: pd.DataFrame):
    print("Counts per year \n\n")
    print(df_in.describe())
    print(df_in)
   
    #df_in.groupby('Funding OrgName').count()
    vals = df_in.groupby('Year Produced', sort=False).size()
    print(vals)





def main():


    df_all_data = pd.read_csv(filepath_or_buffer="data/gtr_raw_data.csv", 
                              index_col='GTR OutcomeId', 
                              header=0)
    
    # Counts per funder

    df_funder = pd.DataFrame(df_all_data, columns=['Funding OrgName'])
    count_per_funder(df_funder)

    # Counts per PI using PIId (orcid is missing a lot)
    df_funder = pd.DataFrame(df_all_data, columns=['PIId'])
    count_per_PI(df_funder)

    # Counts per Research Organisation (lead)
    df_RO = pd.DataFrame(df_all_data, columns=['LeadRO Name'])
    count_per_RO(df_RO)

    
    # Counts per Research Organisation (lead)
    df_os = pd.DataFrame(df_all_data, columns=['Software Open Sourced?'])
    df_os.fillna('No/missing', inplace=True)
    count_per_open_sourced(df_os)

    # Counts per Research Organisation (lead)
    df_year = pd.DataFrame(df_all_data, columns=['Year Produced'])
    count_per_year(df_year)


    # Get count of each http response code
    #df_responses = get_dataframe_from_csv('./data/responses.csv')

    #print(df_responses.groupby(1).count())

if __name__ == '__main__':
    main()