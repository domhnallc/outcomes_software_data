import pandas as pd
import matplotlib.pyplot as plt

import config as cfg

#######################
# count of cats       #
#######################

cols = ["url", "category"]

with open(cfg.categories_file) as data_in:
    df = pd.read_csv(data_in, names=cols, index_col="url").fillna("missing")


df_grouped_cat_count = (
    df.groupby(["category"])
    .size()
    .to_frame("dfcount")
    .sort_values(by="dfcount", ascending=False)
)
df_grouped_cat_count.reset_index("category")
print("\n\nGrouped Cat Count\n\n", df_grouped_cat_count)
df_grouped_cat_count.to_csv(f"{cfg.results_folder}/grouped_cat_count.csv")

#############################
# count of cats  no missing #
#############################

# with missing url removed
df_grouped_cat_count_no_missing = df.query("category != 'missing'")
urls_no_missing = df_grouped_cat_count_no_missing.count()
# TODO is total here including missing?  Should it?
print("\n\n\n")
print(
    "Total URLs ",
)
total_count = df.index.size


print("total software", total_count)
print("missing url ", total_count - urls_no_missing)
print("\n\n\n")

#############################
# count of cats - top 10 fig#
#############################
df_grouped_cat_count.head(10).plot.pie(
    y="dfcount",
    title="Count of software in each category",
    legend=False,
    autopct="%1.1f%%",
    startangle=0,
    textprops={"fontsize": 17},
)


# print(df_grouped_cat_count)
plt.title("Top 10 URL Categories", fontsize=20)
plt.ylabel("")
plt.yticks(fontsize=30)
plt.show()


# Analysis of only 200 code urls

with open(f"{cfg.results_folder}/cats_only_200.csv") as data_in:
    df_200_only_cats = pd.read_csv(
        data_in, names=["url", "response"], index_col=0
    ).fillna("missing")

print("\n\n\nONLY 200\n\n\n", df_200_only_cats)

df_200_group = (
    df_200_only_cats.groupby(["response"]).size().sort_values(ascending=False)
)
print(df_200_group.head(10))
df_200_group.to_csv("./group_only_200_cats.csv")
df_200_group.head(10).plot.pie(
    y="response",
    title="Analysis of URLs with 2** response",
    legend=False,
    autopct="%1.1f%%",
    startangle=0,
    textprops={"fontsize": 17},
)
plt.show()


# breakdown of public commercial code repo

df_grouped_pub_comm_repo = df.loc[df["category"] == "public_commercial_code_repo"]

# print(df_grouped_pub_comm_repo)

githubcom_count = []
bitbucket_count = []
gitlab_count = []
sourceforge_count = []
codegoogle_count = []
other_count = []

names = ["Github", "Bitbucket", "GitLab", "SourceForge", "Google Code", "other"]

for x in df_grouped_pub_comm_repo.index:
    if "github.com" in x:
        githubcom_count.append(x)
    elif "bitbucket" in x:
        bitbucket_count.append(x)
    elif "gitlab" in x:
        gitlab_count.append(x)
    elif "sourceforge" in x or "sf.net" in x:
        sourceforge_count.append(x)
    elif "google" in x or "googlecode" in x:
        codegoogle_count.append(x)
    else:
        other_count.append(x)

counts = [
    len(githubcom_count),
    len(bitbucket_count),
    len(gitlab_count),
    len(sourceforge_count),
    len(codegoogle_count),
    len(other_count),
]


# % of total urls per public commercial repo

# TODO should this include missing?
print("\n\n % of total urls per public commercial repo (including missing)\n\n")
df_breakdown = pd.DataFrame(data=[counts], columns=[names]).T
df_breakdown["% of total software"] = 100 * df_breakdown / total_count
df_breakdown["% of total urls"] = (
    100 * (df_breakdown.apply(lambda x: x - 2063)) / total_count
)
print(df_breakdown)
df_breakdown.to_csv("./output/breakdown_per_public_code_repo.csv")


# TODO can we get use of github over time

df_all_data = pd.read_csv(
    filepath_or_buffer=f"{cfg.main_data_csv}", index_col="GTR OutcomeId", header=0
)
print(df_all_data.keys())
df_year_url = df_all_data[["Url", "Year Produced"]]


df_merge = pd.merge(
    df_grouped_pub_comm_repo, df_year_url, left_on="url", right_on="Url"
)

print(df_merge)

## can we do an analysis of institutes that do have software ability in repository for returns that arent institutional
## IE could put it in repository but dont
