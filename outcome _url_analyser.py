import csv
import pandas as pd

with open("outcomes_software_urls.csv") as data_in:
    df = pd.read_csv(data_in)

print(df)

for url in df.Url:
    print(url)
