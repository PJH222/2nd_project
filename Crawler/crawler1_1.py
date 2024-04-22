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
from multiprocessing import  Manager, Process, freeze_support
from multiprocessing import Pool as ThreadPool
import warnings
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import concurrent.futures


warnings.filterwarnings('ignore')

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

# keywords = ["어느 병원", "어떤 병원", "어디 병원", "무슨 병원", "병원 어디", "어느 진료과", "어떤 진료과", "어디 진료과", "무슨 진료과", "진료과 어디"]
# keywords1 = ["어느 병원", "어떤 병원"]
# keywords2 = ["어디 병원", "무슨 병원"]
# keywords3 = ["병원 어디", "어느 진료과"]
# keywords4 = ["어떤 진료과", "어디 진료과"]
# keywords5 = ["무슨 진료과", "진료과 어디"]

def find_title_contents(links): # 뽑은 링크 내에 제목과 답변 내용 csv에 작성하기
    global csv_writer 
    driver.get(links)
    
    driver.implicitly_wait(10)
    time.sleep(uniform(0.1, 0.2))
    page_soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.implicitly_wait(10)
    
    
    title = page_soup.find('div', class_='title').text.strip()
    question = page_soup.find('div', class_='c-heading__content').text.strip()
    answers = [ans.text.strip() for ans in page_soup.find_all('div', class_='se-main-container')]
    if answers:
        csv_writer.writerow([title, question, answers[0]])
        for answer in answers[1:]:
            csv_writer.writerow(["", "", answer])
    else:
        csv_writer.writerow([title, question, ""])

def inside_site(urls):
    for url in urls:
        driver.get(url)
        driver.implicitly_wait(10) 
        time.sleep(uniform(0.1, 0.2))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = [tag['href'] for tag in soup.find_all('a', class_="_nclicks:kin.txt _searchListTitleAnchor")]        
    return links


for i in range(1):
    keyword = '어떤 병원'
    sort = 'date'
    year = 2019
    month = 12
    day = 11

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
        a = str(datetime.datetime.strptime(start_date,"%Y.%m.%d").date()).replace("-",".")
        b = str(datetime.datetime.strptime(end_date,"%Y.%m.%d").date()).replace("-",".")

        filename = f"{keyword.replace(' ', '_')}/kin_{a}_{b}.csv"    
        ensure_dir(filename)

        try:
            options = webdriver.ChromeOptions()
            options.headless = True
            # options.add_argument('headless')
            options.add_argument('window-size=1920x1080')

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            csv_file = open(filename, mode='w', newline='', encoding='utf-8')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['제목', '질문', '답변'])
            page = 1
            while True:
                url_list = []
                for i in range(10):
                    url = create_search_url(keyword, page, a, b, sort)
                    url_list.append(url)
                    page += 1
                    links_links = []

                
                with ThreadPoolExecutor(max_workers=4) as executor:
                    thread_list = []
                    # links = map(inside_site,url_list)
                    for url in map(inside_site,url_list):
                        thread_list.append(executor.map(find_title_contents, url))

                    
                    # inside_site(url_list)
                    # print(links)
                    # for i in url_list:    
                    #     driver.get(i)
                    #     driver.implicitly_wait(10) 
                    #     time.sleep(uniform(0.1, 0.2))
                    #     soup = BeautifulSoup(driver.page_source, "html.parser")
                    #     links = [tag['href'] for tag in soup.find_all('a', class_="_nclicks:kin.txt _searchListTitleAnchor")]                
                    for execution in concurrent.futures.as_completed(thread_list):
                        execution.result()                       
                        
                cnt = 1
                        
                # with ThreadPoolExecutor(max_workers=4) as executor:
                #     # map(find_title_contents,links)
                #     thread_list = []
                #     for url in links:
                #         thread_list.append(executor.map(find_title_contents, url))
                #         # execution.result()
                        
                #     print()
                #     print("추가 생성된 파일 개수 :",cnt)
                #     print("현재 크롤링 중인 page :",page)
                #     print("현재 진행 중인 기간",a,"~",b)
                #     print() 
                             
                #     cnt += 1                         
                        
                #     for execution in concurrent.futures.as_completed(thread_list):
                #         execution.result()

                # for link in links:
                #     driver.get(link)
                #     time.sleep(uniform(0.88, 1.18))
                #     page_soup = BeautifulSoup(driver.page_source, "html.parser")
                #     title = page_soup.find('div', class_='title').text.strip()
                #     question = page_soup.find('div', class_='c-heading__content').text.strip()
                #     answers = [ans.text.strip() for ans in page_soup.find_all('div', class_='se-main-container')]
                #     if answers:
                #         csv_writer.writerow([title, question, answers[0]])
                #         for answer in answers[1:]:
                #             csv_writer.writerow(["", "", answer])
                #     else:
                #         csv_writer.writerow([title, question, ""])
                # page += 1
                # print(i, page)
                
                # print()
                # print("추가 생성된 파일 개수 :",i + 1)
                # print("현재 크롤링 중인 page :",page)
                # print("현재 진행 중인 기간",a,"~",b)
                # print()
                
                if page > 110:
                    break
                
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            csv_file.close()
            driver.quit()
            print("File has been saved and driver closed.")