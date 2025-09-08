import pandas as pd

def generate_course_url(ccode, year=113, semester=2):
    """根據課程代碼生成對應的 URL"""
    if pd.isna(ccode) or len(str(ccode)) < 9:
        return ""  # 處理無效的課程代碼
    
    ccode = str(ccode)
    ccode_1 = ccode[:6]
    ccode_2 = ccode[6:8] 
    ccode_3 = ccode[8]
    
    url = f"https://newdoc.nccu.edu.tw/teaschm/{year}{semester}/schmPrv.jsp-yy={year}&smt={semester}&num={ccode_1}&gop={ccode_2}&s={ccode_3}.html"
    return url

# 設定顯示選項
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# 讀取 CSV 檔案
df = pd.read_csv("CoursesList.csv", dtype={0: str})

# 假設課程代碼在第一欄，你可能需要調整欄位名稱
# 如果你知道確切的欄位名稱，請替換 df.iloc[:, 0]
course_code_column = df.iloc[:, 0]  # 或者用 df['課程代碼'] 如果有欄位名稱

# 生成 URL 並加入新欄位
df['course_url'] = course_code_column.apply(generate_course_url)

# 直接覆寫原檔案
df.to_csv("CoursesList.csv", index=False, encoding="utf-8-sig")

print("處理完成！URL 已新增至原檔案 CoursesList.csv")
print(f"總共處理了 {len(df)} 筆資料")

# 顯示前幾筆資料作為確認
print("\n前 5 筆資料預覽：")
print(df[['course_url']].head())

# 測試：顯示第二筆資料的 URL（對應你原本的測試）
if len(df) > 1:
    print(f"\n第二筆資料的 URL：")
    print(df.iloc[1]['course_url'])
