# 爬 https://sdgs.un.org/goals 

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DefaultMarkdownGenerator, PruningContentFilter
import pandas as pd
import re

# prune_filter = PruningContentFilter(
#     threshold=0.5,
#     threshold_type="fixed",  # or "dynamic"
#     min_word_threshold=50
# )



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
                    options={"ignore_links": True, "ignore_images": True}
                )
            )
        )

        # Print the extracted content
        return filter_targets_indicators(result.markdown)
        # print("\n" + "="*80 + "\n")


##  Targets and Indicators

def filter_targets_indicators(markdown_text):
    """
    Extracts the 'Targets and Indicators' section from the markdown text.
    """
    try:
        # Use regex to find the section between "##  Targets and Indicators" and "##  Progress and Info"
        pattern = r"(##  Targets and Indicators.*?)##  Progress and Info"
        match = re.search(pattern, markdown_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return "Could not find the 'Targets and Indicators' section."
    except Exception as e:
        return f"An error occurred: {e}"

# data = asyncio.run(main("https://sdgs.un.org/goals/goal1#targets_and_indicators"))
# print(data)



for i in range(1, 18):
    md = asyncio.run(main(f"https://sdgs.un.org/goals/goal{i}#targets_and_indicators"))
    with open('goals.md', 'a', encoding='utf-8') as f:
        f.write(f"# Goal {i}\n\n")
        f.write(md + "\n\n")



# with open('goal1.md', 'r', encoding='utf-8') as f:
#     data = f.read()
#
# filtered_data = filter_targets_indicators(data)
# print(filtered_data)



# # 設定顯示選項
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
#
