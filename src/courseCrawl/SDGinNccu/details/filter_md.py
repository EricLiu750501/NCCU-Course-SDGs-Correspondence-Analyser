from pathlib import Path
import re


def filter_markdown_content(markdown_text):
    """
    根據特定標題，從 Markdown 文本中刪除不需要的區塊，
    並同時去除粗體格式。
    """
    # 步驟一：定義需要刪除的區塊標題
    unwanted_sections = [
        "#### 學分數",
        "##  授課方式Teaching Approach",
        "##  評量工具與策略、評分標準成效Evaluation Criteria",
        "##  指定/參考書目Textbook & References",
        "##  本課程可否使用生成式AI工具Course Policies on the Use of Generative AI Tools",
        "###  課程相關連結Course Related Links",
        "###  課程附件Course Attachments",
        "####  講述 Lecture",
        "####  討論 Discussion",
        "####  小組活動 Group activity",
        "####  數位學習 E-learning",
        "###  課程進行中，使用智慧型手機、平板等隨身設備 To Use Smart Devices During the Class",
        "###  授課教師Office Hours及地點Office Hours & Office Location",
        "###  教學助理基本資料Teaching Assistant Information",
        "Powered by NCCU Computer Center",
        "列印"
    ]
    
    # 使用正規表達式匹配整個區塊，從標題開始到下一個標題或文件結尾
    # 這裡我們使用一個強力的模式，直接匹配所有要刪除的標題，
    # 並將其後直到下一個 H2 標題的內容都納入匹配範圍。
    pattern = '|'.join([re.escape(s) for s in unwanted_sections])
    
    # 正規表達式解釋：
    # (?s) 讓 . 匹配所有字元，包括換行。
    # (?:\s*<br>)*\s* 會匹配任何換行、空格或 <br> 標籤，以處理標題後的空白。
    # (?:<h\d>.*?</h\d>|\n##|\n###|$) 這部分是界定下一個區塊的開始。
    full_pattern = r'(?s)(?:' + pattern + r').*?(?=\n##|\n###|$)'
    
    # 步驟二：刪除不想要的區塊
    filtered_text = re.sub(full_pattern, '', markdown_text)
    
    # 步驟三：去除 Markdown 粗體標記
    # 匹配 **...** 和 __...__ 並保留中間的內容
    filtered_text = re.sub(r'\*\*(.*?)\*\*', r'\1', filtered_text)
    filtered_text = re.sub(r'__(.*?)__', r'\1', filtered_text)
    
    # 步驟四：去除一些固定的多餘行
    lines = filtered_text.splitlines()
    filtered_lines = [line for line in lines if not line.strip() in ['列印', 'Powered by NCCU Computer Center', '* * *', '']]
    
    return "\n".join(filtered_lines).strip()




target_folder = "./"
for file_path in Path(target_folder).glob('*'):
    if file_path.is_file():
        if file_path.suffix == ".md":
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(filter_markdown_content(content))




