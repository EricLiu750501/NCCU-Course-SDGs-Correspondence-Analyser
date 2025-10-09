import pandas as pd
import json

# 讀取 CSV

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

df = pd.read_csv("CoursesList.csv")


def all_department():
    # 取出「開課系級」欄位（去除空白和重複值）
    # departments = df["開課系級\nDepartment and Level / Course School/Department"].dropna().unique()
    departments = df["Unnamed: 7"].dropna().unique()

    # 排序後輸出
    departments = sorted([d.strip() for d in departments])
    for d in departments:
        print(d)


# # 欄位名稱可能含有換行符號，先找出正確名稱
# for col in df.columns:
#     print(col)


def select_department(filter_list=None):
    """
    篩選開課系級包含指定關鍵字的課程
    
    Args:
        filter_list: 字串或字串列表，包含篩選關鍵字
    
    Returns:
        pandas.Series: 符合條件的課程代號列表
    """
    if filter_list is None:
        filter_list = []
    elif isinstance(filter_list, str):
        filter_list = [filter_list]  # 轉換單一字串為列表
        
    # 建立初始遮罩 (全為 False)
    mask = pd.Series([False] * len(df))
    
    # 對每個過濾條件進行篩選，使用 OR 運算累加結果
    for filter_str in filter_list:
        mask = mask | df["開課系級\nDepartment and Level / Course School/Department"].str.contains(filter_str, na=False)

    # 取出符合條件的科目代號
    result = df.loc[mask, "科目代號\nCourse #"]
    return result



# with open("地政課程.json", "w", encoding="utf-8") as f:
#     json.dump(result.tolist(), f, ensure_ascii=False, indent=2)

College_of_Commerce = ["金融", "國貿", "會計", "統計", "企", "資管", "財管", "風管", "商", "科智", "科博"]


if __name__ == "__main__":
    # all_department()
    result = select_department(College_of_Commerce)

    # result = select_department("社會")
    # result = select_department("地") # 地政系

    # result = select_department(["資安", "資碩", "資訊", "資科"])
    print(list(result))
    
    with open("College_of_Commerce.json", "w", encoding="utf-8") as f:
        json.dump(result.tolist(), f, ensure_ascii=False, indent=2)

    # print(f"共 {len(result)} 筆資料")
    #
    # with open("資訊課程.json", "w", encoding="utf-8") as f:
    #     json.dump(result.tolist(), f, ensure_ascii=False, indent=2)

