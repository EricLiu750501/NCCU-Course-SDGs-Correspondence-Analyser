from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import json
from typing import Any, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException

# 從每一個 Scholar 的網址中提取資料

def get_scholar_info(url):
    try:
        # 設置 Chrome 選項
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # 可選：無頭模式
        chrome_options.add_argument("--disable-gpu")
        
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
        print(f"{url} 中找到 {len(tables)} 個 <table class='scholar-id'>")
        
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
                        if value:
                            # 檢查是否有英文逗號（英文版）
                            if ',' in value:
                                expertise_list = [item.strip() for item in value.split(',') if item.strip()]
                            # 檢查是否有中文頓號或小頓號（中文版）
                            elif '、' in value or '﹑' in value:
                                value = value.replace('、', ',').replace('﹑', ',')
                                expertise_list = [item.strip() for item in value.split(',') if item.strip()]
                            # 檢查是否有空格（中文版常見）
                            elif ' ' in value:
                                expertise_list = [item.strip() for item in value.split(' ') if item.strip()]
                            # 無分隔符號，作為單一項目
                            else:
                                expertise_list = [value]
                        info['expertise'] = expertise_list
                    
                    
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
                                publications.append(pub)
                    
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

def restructure_data(scholars:list):
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
    # 讀取 URL
    try:
        with open("./scholars_url.txt", 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("錯誤：找不到 scholars_url.txt")
        exit()
    
    scholars_data = []
    cnt = 0
    
    # 只處理前 5 個 URL
    for url in urls:
        cnt += 1
        if cnt > 50:
            break
        print(f"\n正在處理: {url}")
        info = get_scholar_info(url)
        if info:
            scholars_data.append(info)

    # info = get_scholar_info("https://ah.lib.nccu.edu.tw/scholar?id=9794&locale=en&locale=en")
    # if info:
    #     scholars_data.append(info)

    scholars_data = restructure_data(scholars_data)
    
    # 儲存結果為 JSON
    with open("./scholars_info.json", 'w', encoding='utf-8') as f:
        json.dump(scholars_data, f, ensure_ascii=False, indent=4)
    
    print("\n資訊已儲存到 scholars_info.json")
