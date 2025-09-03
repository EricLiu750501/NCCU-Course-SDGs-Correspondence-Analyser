import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def main():
    browser_conf = BrowserConfig(headless=True, verbose=True)

    run_conf = CrawlerRunConfig()  # 先不用 extraction，直接拿 HTML

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url="https://newdoc.nccu.edu.tw/teaschm/1131/schmPrv.jsp-yy=113&smt=1&num=356373&gop=00&s=1.html",
            config=run_conf
        )

        # 把 HTML 存下來，檢查是否真的包含"授課老師"
        with open("raw1.html", "w", encoding="utf-8") as f:
            f.write(result.html)

        print("✅ 已存 raw.html，請用瀏覽器打開檢查內容")

if __name__ == "__main__":
    asyncio.run(main())
