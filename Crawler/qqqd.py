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
from multiprocessing import Manager, Process, freeze_support

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

def crawl_page(keyword, start_date, end_date, sort, page, output_dir, result_queue):
    try:
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument('window-size=1920x1080')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        a = str(datetime.datetime.strptime(start_date,"%Y.%m.%d").date()).replace("-",".")
        b = str(datetime.datetime.strptime(end_date,"%Y.%m.%d").date()).replace("-",".")
        
        filename = f"{output_dir}/{keyword.replace(' ', '_')}/kin_{a}_{b}.csv"
        ensure_dir(filename)

        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['제목', '질문', '답변'])

            url = create_search_url(keyword, page, a, b, sort)
            driver.get(url)
            driver.implicitly_wait(10)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            links = [tag['href'] for tag in soup.find_all('a', class_="_nclicks:kin.txt _searchListTitleAnchor")]

            for link in links:
                driver.get(link)
                driver.implicitly_wait(10)
                
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
                    
            result_queue.put(filename)
                    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        csv_file.close()
        driver.quit()
        print("File has been saved and driver closed.")

def crawl_keyword(keyword, sort, output_dir, result_queue):
    year = 2020
    month = 6
    day = 16
    
    for i in range(38):
        if day <= 0:
            month -= 1
            day = 31

            if month <= 0:
                month = 12
                year -= 1

        end_date = str(year) + "." + str(month) + "." + str(day)

        if day - 5 <= 0:
            month -= 1
            day = 31

            if month <= 0:
                month = 12
                year -= 1

        start_date = str(year) + "." + str(month) + "." + str(day - 4)

        day = day - 5
        
        for page in range(1, 111):
            p = Process(target=crawl_page, args=(keyword, start_date, end_date, sort, page, output_dir, result_queue))
            p.start()
            p.join()
            print()
            print("추가 생성된 파일 개수 :",i + 1)
            print("현재 크롤링 중인 page :",page)
            print("현재 진행 중인 기간",start_date,"~",end_date)
            print()

            
if __name__ == "__main__":
    freeze_support()
    keyword = '어떤 병원'
    sort = 'date'
    year = 2020
    month = 6
    day = 16
    output_dir = "output"
    result_queue = Manager().Queue() 
    crawl_keyword(keyword, sort, output_dir, result_queue)
