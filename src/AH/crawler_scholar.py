import requests
from bs4 import BeautifulSoup
import re

# 找到所有 Scholar 的網址

def main():
    start_url = "https://ah.lib.nccu.edu.tw/"
    scholar_urls = set()
    for page in range(0, 282):
        print(f"Processing page {page}")
        url = f"https://ah.lib.nccu.edu.tw/browse-scholar-list?page={page}"
    
        # 發送 HTTP GET 請求
        response = requests.get(url)

        # 檢查請求是否成功
        if response.status_code == 200:
            # 解析 HTML 內容
            soup = BeautifulSoup(response.text, 'html.parser')

            
            # 提取所有連結 (範例)
            links_found = 0
            for link in soup.find_all('a', href=True):
                links_found += 1
                url = link['href']
                # # 轉換相對路徑為絕對路徑
                if url.startswith('/'):
                    url = requests.compat.urljoin(start_url, url)
                # # 檢查是否符合 /scholar?id= 的模式
                if re.search(r'/scholar\?id=\d+', url):
                    scholar_urls.add(url+"&locale=en")
                    # print(url)
        else:
            print(f"請求失敗，狀態碼: {response.status_code}")
    

    with open("./scholars_url.txt", 'w') as f:
        for url in scholar_urls:
            f.write(f"{url}&locale=en\n")


if __name__ == "__main__":
    main()
