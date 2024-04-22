import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from datetime import datetime
from random import uniform
from multiprocessing import  Manager, Process, freeze_support
from multiprocessing import Pool as ThreadPool

keyword = '어느 병원'
start_date = '2024.04.02'
end_date = '2024.04.03'
sort = 'date'

def create_search_url(keyword, page, start_date, end_date, sort):
    keyword_encoded = keyword.replace(" ", "+")
    period = f"&period={start_date}.|{end_date}."
    sort_option = f"sort={sort}"
    url = f"https://kin.naver.com/search/list.nhn?query={keyword_encoded}&{sort_option}{period}&section=kin&page={page}"
    return url

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

filename = f"result/kin_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{start_date}_{end_date}.csv"
ensure_dir(filename)

try:
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")

    # browser = webdriver.Chrome(Options=options)
    # browser.maximize_window()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    csv_file = open(filename, mode='w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['제목', '질문', '답변'])

    page = 1
    while True:
        url = create_search_url(keyword, page, start_date, end_date, sort)
        driver.get(url)
        time.sleep(uniform(0.8, 1.2))
        # pool = ThreadPool(4)
        # result = pool.map()
        
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        links = [tag['href'] for tag in soup.find_all('a', class_="_nclicks:kin.txt _searchListTitleAnchor")]
        
        
        if not links:
            break
        
        for link in links:
            driver.get(link)
            time.sleep(uniform(0.8, 1.2))
            page_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            title = page_soup.find('div', class_='title').text.strip()
            question = page_soup.find('div', class_='c-heading__content').text.strip()
            answers = [ans.text.strip() for ans in page_soup.find_all('div', class_='se-main-container')]
            
            if answers:
                csv_writer.writerow([title, question, answers[0]])
                for answer in answers[1:]:
                    csv_writer.writerow(["", "", answer])
            else:
                csv_writer.writerow([title, question, ""])
        
        page += 1
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    csv_file.close()
    driver.quit()
    print("File has been saved and driver closed.")
