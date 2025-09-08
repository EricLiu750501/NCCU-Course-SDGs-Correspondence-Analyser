import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DefaultMarkdownGenerator, PruningContentFilter
import pandas as pd

# prune_filter = PruningContentFilter(
#     threshold=0.5,
#     threshold_type="fixed",  # or "dynamic"
#     min_word_threshold=50
# )

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



async def main(url):
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                markdown_generator=DefaultMarkdownGenerator(
                    # content_filter=PruningContentFilter(
                    #     threshold=0.5,
                    #     threshold_type="dynamic",  # or "dynamic"
                    #     min_word_threshold=50
                    # ),
                    options={"ignore_links": True}
                )
            )
        )

        # Print the extracted content
        return result.markdown
        # print("\n" + "="*80 + "\n")

# # Run the async main function
# lst = ["https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=000221&gop=00&s=1.html", 
#        "https://newdoc.nccu.edu.tw/teaschm/1141/schmPrv.jsp-yy=114&smt=1&num=031023&gop=00&s=1.html"]
# for url in lst:
#     asyncio.run(main(url))


# 設定顯示選項
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# 讀取 CSV 檔案
df = pd.read_csv("CoursesList.csv")

# 假設課程代碼在第一欄，你可能需要調整欄位名稱
# 如果你知道確切的欄位名稱，請替換 df.iloc[:, 0]
course_code_column = df.iloc[:, 0]  # 或者用 df['課程代碼'] 如果有欄位名稱

urls = course_code_column.apply(generate_course_url).tolist()

for i in range(len(urls)):
    md = asyncio.run(main(urls[i]))
    filepath = f"details/{course_code_column[i]}.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md) 



