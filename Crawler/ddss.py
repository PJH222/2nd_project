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
from multiprocessing import Process, Queue
from selenium.webdriver.common.keys import Keys
import warnings

warnings.filterwarnings('ignore')

def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def create_search_url(keyword, page, start_date, end_date, sort):
    keyword_encoded = keyword.replace(" ", "+")
    period = f"&period={start_date}.|{end_date}."
    sort_option = f"sort={sort}"
    url = f"https://kin.naver.com/search/list.nhn?query={keyword_encoded}&{sort_option}{period}&section=kin&page={page}"
    return url

def crawl_page(keyword, start_date, end_date, sort, page, queue):
    global a,b
    csv_file = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x1080')
        options.add_experimental_option("detach", True)

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
            queue.put(link)  # 링크를 큐에 추가합니다.

        # driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if csv_file is not None:
            csv_file.close()
        driver.quit()

def crawl_keyword(keyword, start_date, end_date, sort, queue):
    for page in range(1, 111):
        crawl_page(keyword, start_date, end_date, sort, page, queue)
        print()
        print("현재 크롤링 중인 page와 keyword :", page, keyword[:5] if keyword[5] != "" else keyword[:6])
        print("현재 진행 중인 기간", a, "~", b)
        print()

if __name__ == "__main__":
    keywords = ["어느 병원", "어떤 병원"]
    start_date = "2020.01.01"
    end_date = "2020.12.31"
    sort = 'date'

    ensure_dir("output")

    queue = Queue()  # 큐 생성

    processes = []
    for keyword in keywords:
        p = Process(target=crawl_keyword, args=(keyword + " -동물 -성형 -강아지 -피부과 -개인회생 -인테리어 -진로 -커리큘럼 -자동차 -도서 -보험 -교통 -차 -탈모 -간호학과 ", start_date, end_date, sort, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not queue.empty():  # 큐가 비어있지 않은 동안 반복
        link = queue.get()  # 큐에서 링크를 가져옴
        print("Processing link:", link)
        # 링크를 처리하는 작업을 수행합니다.
        # 이 부분에 링크를 처리하는 함수를 호출하면 됩니다.
