import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
# from datetime import datetime
import datetime
from random import uniform
from multiprocessing import  Manager, Process, freeze_support
from multiprocessing import Pool as ThreadPool

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


# nows = datetime.datetime.strptime("2023-07-16","%Y-%m-%d")

# # for i in range(5):
# start_date = nows - datetime.timedelta(days=5)
# end_date = datetime.datetime.date(nows)
keyword = '어느 병원'
start_date = '2023.03.05'
end_date = '2023.03.09' 
sort = 'date'

filename = f"result/kin_{keyword.replace(' ', '_')}_{start_date}_{end_date}.csv"    
ensure_dir(filename)
try:
    # options = Options()
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    # options.add_argument("window-size=1920x1080")

    # options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    csv_file = open(filename, mode='w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['제목', '질문', '답변'])
    page = 1
    while True:
        url = create_search_url(keyword, page, start_date, end_date, sort)
        driver.get(url)
        time.sleep(uniform(1.0, 1.3))
        # pool = ThreadPool(4)
        # result = pool.map()
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = [tag['href'] for tag in soup.find_all('a', class_="_nclicks:kin.txt _searchListTitleAnchor")]
        if not links:
            break
        
        for link in links:
            driver.get(link)
            time.sleep(uniform(1.0, 1.3))
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
        print(page)
        if page > 110:
            break
        
except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    csv_file.close()
    driver.quit()
    print("File has been saved and driver closed.")