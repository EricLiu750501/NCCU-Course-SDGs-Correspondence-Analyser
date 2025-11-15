import pandas as pd
import json

df = pd.read_csv("./113-2.xlsx - 工作表1.csv")

lst  = df['科目代號'].tolist()

json.dump(lst, open("1132_courselist.json","w"), indent=2, ensure_ascii=False)

