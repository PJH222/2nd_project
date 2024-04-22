import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import datetime
from random import uniform
import threading
from multiprocessing import Process, Queue


def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        
def create_search_url(keyword, page, start_date, end_date, sort):
    keyword_encoded = keyword.replace(" ", "+")
    period = f"&period={start_date}.|{end_date}."
    sort_option = f"sort={sort}"
    url = f"https://kin.naver.com/search/list.nhn?query={keyword_encoded}&{sort_option}{period}&section=kin&page={page}"
    return url

visited_links = set()

def crawl_page(keyword, start_date, end_date, sort, page):
    global a, b, driver, csv_writer
    
    csv_file = None
    try:
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        a = datetime.datetime.strptime(start_date, "%Y.%m.%d").strftime("%Y.%m.%d")
        b = datetime.datetime.strptime(end_date, "%Y.%m.%d").strftime("%Y.%m.%d")
        directory = f"output/{keyword.replace(' ', '_')}"
        ensure_dir(directory)

        filename = f"{directory}/kin_{a}_{b}.csv"
        mode = 'a' if os.path.exists(filename) else 'w'
        
        csv_file = open(filename, mode=mode, newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        if mode == 'w':
            csv_writer.writerow(['제목', '질문', '답변'])

        url = create_search_url(keyword, page, a, b, sort)
        driver.get(url)
        driver.implicitly_wait(10)

        time.sleep(uniform(0.1, 0.19))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = [tag['href'] for tag in soup.find_all('a', class_="_nclicks:kin.txt _searchListTitleAnchor")]

        for link in links:
            if link in visited_links:
                continue
            visited_links.add(link)
        # print(visited_links)
        print(len(visited_links))
        queue = Queue()
        processes = []
        for link in links:
            p = Process(target=find_information, args=(link,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()
            # thread = threading.Thread(target=find_information, args = (link,))
            # thread.start()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if csv_file is not None:
            csv_file.close()

def crawl_keyword(keyword, start_date, end_date, sort):
    for page in range(1, 111):
        crawl_page(keyword, start_date, end_date, sort, page)
        print()
        print("현재 크롤링 중인 page :", page)
        print("현재 진행 중인 기간", a, "~", b)
        print() 
        
def find_information(link):
    driver.get(link)
    driver.implicitly_wait(10)
    time.sleep(uniform(0.1, 0.18))
    
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

if __name__ == "__main__":
    keywords = ["어느 병원", "어떤 병원"]
    start_date = "2020.01.01"
    end_date = "2020.12.31"
    sort = 'date'
    
    ensure_dir("output")
    
    for keyword in keywords:
        crawl_keyword(keyword +" -동물 -성형 -강아지 -피부과 -개인회생 -인테리어 -진로 -커리큘럼 -자동차 -도서 -보험 -교통 -차 -탈모 -간호학과 ", start_date, end_date, sort)
        
