from pathlib import Path
import re
def filter_markdown_content(markdown_text):
    """
    根據特定標題，從 Markdown 文本中刪除不需要的區塊，
    並同時去除粗體格式。
    """
    # 步驟一：定義需要刪除的區塊標題
    unwanted_sections = [
        "