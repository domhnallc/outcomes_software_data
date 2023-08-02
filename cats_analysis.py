import pandas as pd
import matplotlib.pyplot as plt

cols = ["url", "category"]

with open("./cats.csv") as data_in:
    df = pd.read_csv(data_in, names=cols, index_col="url").fillna("missing")

df_grouped_cat_count = (
    df.groupby(["category"])
    .size()
    .to_frame("dfcount")
    .sort_values(by="dfcount", ascending=False)
)
df_grouped_cat_count.reset_index("category")
print(df_grouped_cat_count)

total_count = df.index.size
print("total unique urls", total_count)

df_grouped_cat_count.head(10).plot.pie(
    y="dfcount", title="Title", legend=False, autopct="%1.1f%%", startangle=0
)
# print(df_grouped_cat_count)
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
df_breakdown = pd.DataFrame(data=[counts], columns=[names]).T
df_breakdown["% of total urls"] = 100 * df_breakdown / total_count


print(df_breakdown)


# TODO can we get use of github over time
