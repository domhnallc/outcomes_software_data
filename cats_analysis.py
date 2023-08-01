import pandas as pd
import matplotlib.pyplot as plt

cols = ["url", "category"]

with open("./cats.csv") as data_in:
    df = pd.read_csv(data_in, names=cols, index_col="url").fillna("missing")


    df_grouped_cat_count = df.groupby(["category"]).size().to_frame("dfcount").sort_values(by="dfcount", ascending=False)
    df_grouped_cat_count.reset_index("category")
    
    df_grouped_cat_count.plot.pie(y="dfcount", title="Title", legend=False, autopct='%1.1f%%', startangle=0)
    #print(df_grouped_cat_count)
    plt.show()

