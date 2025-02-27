import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import seaborn as sns
import helper as hlp
import config as cfg


"""gtr_raw_data.csv headers:
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
"""


def main():
    # load in all data
    df_all_data = pd.read_csv(
        filepath_or_buffer=cfg.main_data_csv, index_col="GTR OutcomeId", header=0,dtype={'Year Produced': str}
    )

    # Counts per funder
    df_funder = pd.DataFrame(df_all_data, columns=["Funding OrgName"])
    funder = hlp.count_per_funder(df_funder)
    hlp.print_out("Counts per funder", funder)
    if cfg.latex:
        print(funder.to_latex())

    # Counts per PI using PIId (orcid is missing a lot)
    df_PrincipleInv = pd.DataFrame(df_all_data, columns=["PIId"])
    hlp.print_out("Counts per PI", hlp.count_per_PI(df_PrincipleInv))
    if cfg.latex:
        print(df_PrincipleInv.to_latex())

    # Counts per Research Organisation (lead)
    df_RO = pd.DataFrame(df_all_data, columns=["LeadRO Name"])
    hlp.print_out("Counts per RO", hlp.count_per_RO(df_RO))
    hlp.count_per_RO(df_RO).to_csv(f"{cfg.results_folder}/count_per_ro.csv")
    if cfg.latex:
        print(df_RO.to_latex())

    # Counts per open source
    df_os = pd.DataFrame(df_all_data, columns=["Software Open Sourced?"])
    df_os.fillna("No/missing", inplace=True)
    hlp.print_out("Counts of Open Source", hlp.count_per_open_sourced(df_os))

    # Counts per year
    df_year = pd.DataFrame(df_all_data, columns=["Year Produced"])
    total_count_year = hlp.count_per_year(df_year)
    hlp.print_out("Counts per year", total_count_year)
    total_count_year.plot()
    plt.ylabel("Count of Software")
    plt.xlabel("Year of Output")
    plt.show()

    # Counts per dept
    df_dept = pd.DataFrame(df_all_data, columns=["Department"])
    hlp.print_out("Counts per dept", hlp.count_per_department(df_dept))

    # Get count of each http response code
    df_responses = hlp.get_dataframe_from_csv(f"{cfg.results_folder}/responses.csv")

    print(df_responses.groupby(1).count())
    df_responses.groupby(1).count().to_csv(f"{cfg.results_folder}/http_responses.csv")

    df_responses.groupby(1).count().plot.pie(
        y=0,
        title="Count per http response",
        legend=False,
        autopct="%1.1f%%",
        startangle=0,
        textprops={"fontsize": 10},
    )

    ## Summarise responses into code families and plot

    response_summary = {"2**": 3946, "4**": 710, "5**": 51, "Non-HTTP Error": 462}
    df_response_summary = pd.DataFrame.from_dict(
        response_summary, orient="index", columns=["Count"]
    )
    print(df_response_summary)
    df_response_summary.plot.pie(
        y="Count",
        title="Title",
        legend=False,
        autopct="%1.1f%%",
        startangle=0,
        textprops={"fontsize": 17},
    )

    ####subanalysis of sware being open sourced

    # dichotomous sware os? per year
    df_os_per_year = pd.DataFrame(
        df_all_data, columns=["Software Open Sourced?", "Year Produced"]
    )
    df_os_per_year.fillna("No/missing", inplace=True)
    print(
        "\n\n\n",
        df_os_per_year.groupby(["Software Open Sourced?", "Year Produced"])[
            "Software Open Sourced?"
        ]
        .count()
        .unstack(level=0),
    )

    # dichotomous sware os? per RO
    df_os_per_ro = pd.DataFrame(
        df_all_data, columns=["Software Open Sourced?", "LeadRO Name"]
    )
    df_os_per_ro.fillna("No/missing", inplace=True)
    print(
        "\n\n\n",
        df_os_per_ro.groupby(["Software Open Sourced?", "LeadRO Name"])[
            "Software Open Sourced?"
        ]
        .count()
        .unstack(level=0),
    )

    # dichotomous sware os? per funder
    df_os_per_funder = pd.DataFrame(
        df_all_data, columns=["Software Open Sourced?", "Funding OrgName"]
    )
    df_os_per_funder.fillna("No/missing", inplace=True)
    print(
        "\n\n\n",
        df_os_per_funder.groupby(["Software Open Sourced?", "Funding OrgName"])[
            "Software Open Sourced?"
        ]
        .count()
        .unstack(level=0),
    )

    # dichotomous sware os? per PI
    df_os_per_PI = pd.DataFrame(df_all_data, columns=["Software Open Sourced?", "PIId"])
    df_os_per_PI.fillna("No/missing", inplace=True)
    print(
        "\n\n\n",
        df_os_per_PI.groupby(["Software Open Sourced?", "PIId"])[
            "Software Open Sourced?"
        ]
        .count()
        .unstack(level=0),
    )

    ####subanalysis of vars over time
    print("\n\n\nsubanalysis of vars over time\n\n\n")

    # ro per year
    df_ro_per_year = pd.DataFrame(df_all_data, columns=["Year Produced", "LeadRO Name"])
    df_ro_per_year.fillna("No/missing", inplace=True)
    df_grouped = (
        df_ro_per_year.groupby(["Year Produced", "LeadRO Name"])["Year Produced"]
        .count()
        .unstack(level=0)
        .astype("Int64")
    )
    print(df_grouped)

    ###################
    # funder per year #
    ###################
    df_funder_per_year = pd.DataFrame(
        df_all_data, columns=["Year Produced", "Funding OrgName"]
    )

    df_grouped = (
        df_funder_per_year.groupby(["Year Produced", "Funding OrgName"])[
            "Year Produced"
        ]
        .count()
        .unstack(level=0)
        .astype("Int64")
        .fillna(0)
    )
    df_grouped.columns = df_grouped.columns.astype(str)
    print(df_grouped)
    df_grouped.to_csv(f"{cfg.results_folder}/funder_per_year.csv")
    # plot
    df_grouped.T.plot()
    plt.ylabel("Count of Software")
    plt.xlabel("Year of Output")
    plt.show()

    # os per year
    df_os_per_year = pd.DataFrame(
        df_all_data, columns=["Year Produced", "Software Open Sourced?"]
    )
    df_grouped_os = (
        df_os_per_year.groupby(["Year Produced", "Software Open Sourced?"])[
            "Year Produced"
        ]
        .count()
        .unstack(level=0)
        .astype("Int64")
        .fillna(0)
    )
    print(df_grouped_os)
    # plot
    df_grouped_os.T.plot()
    # total_count_year.plot()
    plt.show()

    df_merge = pd.concat([df_grouped_os.T, total_count_year], axis=1)
    print(df_merge)
    df_merge.plot()
    plt.xlabel("Year produced", fontsize=20)
    plt.ylabel("Software Count", fontsize=20)
    plt.legend(fontsize=16)

    plt.legend().get_texts()[0].set_text("Open sourced")
    plt.legend().get_texts()[1].set_text("Software count")
    plt.yticks(fontsize=16)
    plt.xticks(
        np.arange(0, len(df_merge) - 1, 1),
        # TODO: def func to find year range to create labels
        labels=[
            2006,
            2007,
            2008,
            2009,
            2010,
            2011,
            2012,
            2013,
            2014,
            2015,
            2016,
            2017,
            2018,
            2019,
            2020,
            2021,
            2022,
            2023,
            2024,
        ],
        fontsize=16,
    )
    plt.show()


if __name__ == "__main__":
    main()
