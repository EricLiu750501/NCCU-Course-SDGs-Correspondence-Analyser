import pandas as pd

df = pd.read_csv("./1141有關氣候科學或環境永續之課程.xlsx - 課表(全).csv")

# 將永續課程欄位只含空白的視為遺失值，先去頭尾空白
df['永續課程'] = df['永續課程'].astype(str).replace(r'^\s*$', pd.NA, regex=True).str.strip()

# 轉成數值（'0' 會變成 0），無法轉的變成 NaN
df['永續課程'] = pd.to_numeric(df['永續課程'], errors='coerce')

# 刪除 '永續課程' 為空的列（保留 0）
df = df.dropna(subset=['永續課程'])

# 如果希望永續課程為整數（沒有小數）
df['永續課程'] = df['永續課程'].astype(int)

# 輸出成 1141.csv（Excel-friendly 編碼）
df[['科目代號', '永續課程']].to_csv('1141.csv', index=False, encoding='utf-8-sig')

print("✅ 已成功輸出 1141.csv")







df = pd.read_csv("./113-2.xlsx - 工作表1.csv")

# 將永續課程欄位只含空白的視為遺失值，先去頭尾空白
df['永續課程'] = df['永續課程'].astype(str).replace(r'^\s*$', pd.NA, regex=True).str.strip()

# 轉成數值（'0' 會變成 0），無法轉的變成 NaN
df['永續課程'] = pd.to_numeric(df['永續課程'], errors='coerce')

# 刪除 '永續課程' 為空的列（保留 0）
df = df.dropna(subset=['永續課程'])

# 如果希望永續課程為整數（沒有小數）
df['永續課程'] = df['永續課程'].astype(int)

# 輸出成 1141.csv（Excel-friendly 編碼）
df[['科目代號', '永續課程']].to_csv('1132.csv', index=False, encoding='utf-8-sig')

print("✅ 已成功輸出 1132.csv")




