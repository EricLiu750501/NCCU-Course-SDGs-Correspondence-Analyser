import pandas as pd
import json

# 讀取 CSV

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)


df = pd.read_csv("../dept_mapping_updated.csv")

print(df[df["college"] == "Unclassified"]["pattern"])

