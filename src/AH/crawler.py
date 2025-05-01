from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, random
import os
import json
from typing import Any, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException
import re

# 從每一個 Scholar 的網址中提取資料
# 3h 20m 19s : 500 urls

def parse_expertise(raw: str) -> list[str]:
    """
    將專長欄位字串轉換為乾淨的 list。
    支援中英文，處理常見分隔符：頓號、逗號，並進一步處理中文專長中間的空格。
    """
    if not raw:
        return []

    # 初步用常見分隔符切開
    primary_separators = r"[、,，]+"
    items = re.split(primary_separators, raw)
    
    result = []
    for item in items:
        item = item.strip()
        if not item:
            continue
        # 如果是「中文字 空格 中文字」，則進一步切開
        if re.search(r"[\u4e00-\u9fff]+\s+[\u4e00-\u9fff]+", item):
            result.extend([s.strip() for s in item.split() if s.strip()])
        else:
            result.append(item)

    return result


def get_scholar_info(url):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    ]
    try:
        # 設置 Chrome 選項
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 可背景執行
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # 指定 ChromeDriver 路徑
        chromedriver_path = './chromedriver-mac-arm64/chromedriver'
        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError(
                f"ChromeDriver 未找到，請確認 {chromedriver_path} 存在。\n"
                "請從 https://googlechromelabs.github.io/chrome-for-testing/ 下載 chromedriver-mac-arm64。"
            )
        
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 訪問頁面並等待載入
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'scholar-id'))
        )        
        # 解析頁面
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        info = {'url': url}
                
        # 診斷
        tables = soup.find_all('table', class_='scholar-id')
        # print(f"{url} 中找到 {len(tables)} 個 <table class='scholar-id'>")
        
        # 提取基本資料（第一個 table）
        if tables:
            basic_table = tables[0]
            rows = basic_table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()
                    if 'Name' in key:
                        info['name'] = value
                    elif 'Title' in key:
                        info['title'] = value
                    elif 'Department' in key:
                        info['department'] = value
                    elif 'College' in key:
                        info['college'] = value
                    elif 'Research Expertise' in key:
                        expertise_list = []
                        value = value.strip()
                        info['expertise'] = parse_expertise(value)
                    
        # 導航到 Periodical Articles 頁面
        publications = []
        try:
            # 找到 Periodical Articles 連結
            periodical_link = soup.find('a', id='jounalTitle')
            if periodical_link:
                periodical_url = urljoin(url, periodical_link['href'])
                driver.get(periodical_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'scholar-id-form'))
                )                
                # 爬取所有出版物頁面
                while True:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # 提取出版物清單
                    pub_table = soup.find('table', class_='scholar-id-form')
                    if pub_table:
                        rows = pub_table.find('tbody').find_all('tr')
                        for row in rows:
                            cols = row.find_all('td')
                            if len(cols) == 4:
                                pub = {}
                                title_link = cols[1].find('a')
                                pub['title'] = title_link.text.strip() if title_link else ''
                                pub['type'] = cols[2].text.strip()
                                publications.append(pub['title'])
                    
                    # 檢查是否有下一頁
                    try:
                        # 使用 CSS 選擇器定位包含 <span class="next"> 的 <a> 標籤
                        next_button = WebDriverWait(driver, 15).until(
                           EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.pagination li a:has(span.next)'))
                        )
                        print("找到下一頁按鈕，嘗試點擊")
                        # 確保按鈕可見
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        
                        try:
                            next_button.click()
                            print("標準點擊成功")
                        except (ElementClickInterceptedException, ElementNotInteractableException):
                            print("標準點擊失敗，嘗試 JavaScript 點擊")
                            driver.execute_script("arguments[0].click();", next_button)
                        
                        # 等待頁面刷新
                        # WebDriverWait(driver, 10).until(
                        #     EC.staleness_of(pub_table)  # 等待舊表格消失
                        # )
                        WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'scholar-id-form'))  # 等待新表格出現
                        )
                    except TimeoutException:
                        print("沒有下一頁或按鈕不可點擊")
                        break
                    except StaleElementReferenceException:
                        print("下一頁按鈕失效，可能頁面已刷新")
                        break
                    except Exception as e:
                        print(f"點擊下一頁時發生錯誤: {str(e)}")
                        break
            else:
                print(f"{url} 未找到 Periodical Articles 連結")
        except Exception as e:
            print(f"無法爬取 {url} 的出版物: {e}")

        driver.quit()
        
        # 將出版物加入資訊
        info['publications'] = publications
        
                    
        
        return info
    
    except Exception as e:
        print(f"無法處理 {url}: {e}")
        return None

def restructure_data(scholars:list) -> dict:
    result = {}
    for scholar in scholars:
        college = scholar['college']
        department = scholar['department']
        
        # 如果 college 不在 result 中，初始化
        if college not in result:
            result[college] = {}
        
        # 如果 department 不在 college 中，初始化
        if department not in result[college]:
            result[college][department] = []
        
        # 將學者資料加入對應的 department
        result[college][department].append({
            'url': scholar['url'],
            'name': scholar['name'],
            'title': scholar['title'],
            'expertise': scholar['expertise'],
            'publications': scholar['publications']
        })
    
    return result




if __name__ == "__main__":
    n = int(input("Please input file number:"))
    # 讀取 URL
    try:
        with open(f"./scholars_url_{n}.txt", 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"錯誤：找不到 scholars_url{n}.txt")
        exit()
    
    scholars_data = []
    cnt = 0

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    url_len = len(urls)
    cnt = 0
    error_times = 0
    error_urls = []
    while cnt < url_len:
        if cnt % 30 == 0 and cnt != 0:  # 每爬 30 頁
            print(f"已處理 {cnt} 個學者資料，暫停中")
            time.sleep(random.uniform(10, 20))
        elif cnt % 300 == 0 and cnt != 0:  # 每爬 300 頁
            print(f"已處理 {cnt} 個學者資料，暫停中")
            time.sleep(random.uniform(40, 50))
        else:
            time.sleep(random.uniform(0.5, 1.5))


        print(f"\n正在處理({cnt})({time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}): {urls[cnt]}")
        info = get_scholar_info(urls[cnt])
        if info:
            scholars_data.append(info)
            cnt += 1
            error_times = 0
        else:
            if error_times >= 3:
                print(f"無法處理 {urls[cnt]}，跳過")
                cnt += 1
                error_times = 0
                error_urls.append(urls[cnt])
            print(f"無法處理 {urls[cnt]}，等待重新處理")
            time.sleep(random.uniform(40, 45))
            error_times += 1





    restructure_scholars_data = restructure_data(scholars_data)
    
    # 儲存結果為 JSON
    with open(f"./scholars_info_{n}.json", 'w', encoding='utf-8') as f:
        json.dump(restructure_scholars_data, f, ensure_ascii=False, indent=4)
    
    print(f"\n資訊已儲存到 scholars_info_{n}.json")
    
    with open(f"./scholars_info_{n}_error_urls.txt", 'w', encoding='utf-8') as f: 
        for url in error_urls:
            f.write(f"錯誤網址: {url}\n")

