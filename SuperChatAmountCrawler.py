#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Install selenium if you don't have
get_ipython().system('pip install selenium')


# In[10]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import time

# 設置 Chrome 選項
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 如果不需要顯示瀏覽器視窗，取消註解這行
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 指定 ChromeDriver 路徑（根據您的實際路徑修改）
# 請自行下載ChromeDriver
chromedriver_path = "E:\chromedriver-win64\chromedriver.exe"  # Windows 用 .exe，Linux/Mac 用 chromedriver

# 初始化瀏覽器
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

print("browser initialize completed")


# In[21]:


def extract_super_thanks_amount(text):
    # 使用正則表達式匹配金額（支援您提供的格式）
    pattern = r"(NT\$|HK\$|￥|\$|A\$|₩|MYR\s+)(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+(?:\.\d{1,2})?)"
    match = re.search(pattern, text)
    
    if match:
        currency = match.group(1).strip()  # 貨幣符號，去除多餘空格
        value = float(match.group(2).replace(",", ""))  # 移除千位分隔符並轉為浮點數
        return currency, value
    return None

#函式範例
def crawl_youtube_super_thanks(video_url):
    # 儲存超級感謝金額
    super_thanks_totals = {}
    
    # 打開影片頁面
    driver.get(video_url)
    time.sleep(3)  # 等待頁面載入
    
    # 滾動頁面以載入更多留言和 Super Thanks
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)  # 等待新內容載入
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:  # 如果沒有新內容，停止滾動
            break
        last_height = new_height
    
    # 抓取 Super Thanks 的金額元素
    super_thanks_elements = driver.find_elements(By.ID, "comment-chip-price")
    
    # 處理每個 Super Thanks 元素
    for element in super_thanks_elements:
        amount_text = element.text.strip()  # 提取金額文字，例如 "NT$830.00"
        amount = extract_super_thanks_amount(amount_text)
        if amount:
            currency, value = amount
            if currency in super_thanks_totals:
                super_thanks_totals[currency] += value
            else:
                super_thanks_totals[currency] = value
    
    return super_thanks_totals

print("函數定義完成！")


# In[12]:


# 輸入 YouTube 影片 URL
#video_url = input("請輸入 YouTube 影片 URL（例如 https://www.youtube.com/watch?v=kOZWQgtqps4）：")
video_url = "https://www.youtube.com/watch?v=oeMkM0FJ2iE"
print(f"\n正在爬取影片: {video_url} 的留言...")
comments, super_thanks_totals = crawl_youtube_comments(video_url)

# 輸出結果
print(f"\n總共找到 {len(comments)} 條留言")
print("\n超級感謝金額統計（按貨幣單位）：")
if super_thanks_totals:
    for currency, total in super_thanks_totals.items():
        print(f"{currency}: {total:.2f}")
else:
    print("未找到任何超級感謝金額。")

# 關閉瀏覽器
#driver.quit()


# In[42]:


# 輸入 YouTube 影片 URL
video_url = "https://www.youtube.com/watch?v=kOZWQgtqps4"

#比較短的影片測試用 318個回覆
#video_url = "https://www.youtube.com/watch?v=oeMkM0FJ2iE"
print(f"\n正在爬取影片: {video_url} 的留言...")

#comments, super_thanks_totals = crawl_youtube_comments(video_url)

# 輸出結果
# print(f"\n總共找到 {len(comments)} 條留言")
# print("\n超級感謝金額統計（按貨幣單位）：")
# if super_thanks_totals:
#     for currency, total in super_thanks_totals.items():
#         print(f"{currency}: {total:.2f}")
# else:
#     print("未找到任何超級感謝金額。")

# 儲存超級感謝金額
super_thanks_totals = {}

# 打開影片頁面
driver.get(video_url)
time.sleep(3)  # 等待頁面載入

# 滾動頁面以載入更多留言和 Super Thanks
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)  # 等待新內容載入
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:  # 如果沒有新內容，停止滾動
        break
    last_height = new_height

# 抓取 Super Thanks 的金額元素
super_thanks_elements = driver.find_elements(By.ID, "comment-chip-price")

for element in super_thanks_elements:
    amount_text = element.text.strip()  # 提取金額文字，例如 "NT$830.00"
    
    amount = extract_super_thanks_amount(amount_text)
    
    if amount:
        currency, value = amount
        if currency in super_thanks_totals:
            super_thanks_totals[currency] += value
        else:
            super_thanks_totals[currency] = value
    print(super_thanks_totals)
print(f"\n總共找到 {len(super_thanks_elements)} 條留言")
print("\n超級感謝金額統計（按貨幣單位）：")
for currency, total in super_thanks_totals.items():
    print(f"{currency}: {total:.2f}")
#return super_thanks_totals

