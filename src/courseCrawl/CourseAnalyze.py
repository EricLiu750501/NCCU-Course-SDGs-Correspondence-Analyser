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

College_of_Commerce = ["金融", "國貿", "會計","會碩" , "統計", "企", "資管", "財管", "風管", "商", "科智", "科博", "國營", "科管智財所", "資博"]
College_of_Law = ["法學院", "法律", "法碩", "法科"]
College_of_Liberal_Arts = ["中文","國教", "歷史", "哲學", "圖", "宗", "台", "華", "文院"]
College_of_Science = ["應數", "心理", "神科", "應物", "電物學程", "輔諮"]
College_of_Social_Science = ["社會", "社工","行管", "行國防" , "行領導", "社科", "政治", "財政", "公行", "地", "經濟", "民族", "國發", "勞工", "社工", "行館", "亞太", "應社", "原碩"]
College_of_Foreign_Languages = ["英文", "阿文", "斯語", "日文", "韓文", "土文", "歐文", "東南", "語言", "外文", "英教", "中東"]
College_of_Communication = ["傳院", "傳播", "傳在" , "新聞", "廣告","廣電", "國傳", "數位", "亞際"]
College_of_International_Affairs = ["外交", "東亞", "俄","日學","日本碩", "國研","戰略","國安", "國務院"]

College_of_Education = ["教育", "幼", "教政","師資培","學行","輔諮", "教院"]
College_of_Education_Exclude = ["教務處通識教育中心"]

International_College_of_Innovation = ["創國","全創"]

College_of_Informatics = ["資訊", "資碩", "資專","數位", "資安","人智", "AI中心", "群智博"]
College_of_Xperimental = ["X實驗學士"]

College_of_Banking_and_Finance = [""]

Bachelor_Program_of_in_Sport = ["運動學程"]

PE_Coures = ["體育"]

Center_for_Creativity = ["創新創造力研究中心"]

else_course = ["國關通", ]



if __name__ == "__main__":
    # all_department()
    result = select_department(College_of_Commerce)

    
    with open("College_of_Commerce.json", "w", encoding="utf-8") as f:
        json.dump(result.tolist(), f, ensure_ascii=False, indent=2)

    # print(f"共 {len(result)} 筆資料")
    #
    # with open("資訊課程.json", "w", encoding="utf-8") as f:
    #     json.dump(result.tolist(), f, ensure_ascii=False, indent=2)

