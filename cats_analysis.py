import pandas as pd
import matplotlib.pyplot as plt

cols = ["url", "cat", "percentage"]

with open("./cats.csv") as data_in:
    df = pd.read_csv(data_in, names=cols, index_col="url").fillna("missing")


    df_grouped_cat_count = df.groupby(["cat"]).size().to_frame("dfcount").reset_index("cat").sort_values(by="dfcount", ascending=False)
    

    print(df_grouped_cat_count)

