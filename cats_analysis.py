import pandas as pd
import matplotlib.pyplot as plt

cols = ["url", "cat"]

with open("./cats.csv") as data_in:
    df = pd.read_csv(data_in, names=cols, index_col="url").fillna("missing")

print(
    df.groupby(["cat"])
    .size()
    .reset_index(name="counts")
    .sort_values(by="counts", ascending=False)
)
