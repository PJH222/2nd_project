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
from multiprocessing import Pool, Manager
import warnings
from multiprocessing import Process, Queue
import queue
from selenium.webdriver.common.keys import Keys

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

visited_links = set()

def crawl_page(keyword, start_date, end_date, sort, page):
    csv_file = None    
    try:
        # aa = time.time()
        options = webdriver.ChromeOptions()
        # print("-1번째 :",time.time() - aa)
        options.headless = True
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('--log-level=3') 
        options.add_argument('--disable-loging')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # print("-2번째 :",time.time() - aa)
        driver = webdriver.Chrome(service=service, options=options)
        # print("0번째 :",time.time() - aa)
 
        tmp = keyword[:5] if keyword[5] != "" else keyword[:6]
        
        directory = f"output/{tmp.replace(' ', '_')}"
        ensure_dir(directory)
        
        filename = f"{directory}/kin_{start_date}_{end_date}.csv"
        mode = 'a' if os.path.exists(filename) else 'w'
                
        # print("1번째 :",time.time() - aa)

        csv_file = open(filename, mode=mode ,newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        
        url = create_search_url(keyword, page, start_date, end_date, sort)
        
        if mode == 'w':
            csv_writer.writerow(['제목', '질문', '답변',url])
        
        # url = create_search_url(keyword, page, start_date, end_date, sort)
        
        # print("2번째 :",time.time() - aa)
        
        driver.get(url)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(uniform(0.05, 0.1))

        # print("3번째 :",time.time() - aa)

        links = [tag['href'] for tag in soup.find_all('a', class_="_nclicks:kin.txt _searchListTitleAnchor")]
            
        # print("4번째 :",time.time() - aa)
        
        # for link in links:
        #     if link in visited_links:
        #         continue
        #     visited_links.add(link)
        # driver.get(link)
        # print(len(visited_links))
        
        for link in links:
            if link in visited_links:
                continue
            visited_links.add(link)
            # print(len(visited_links))
            # print("5번째 :",time.time() - aa)
            driver.get(link)
            driver.implicitly_wait(10)
            time.sleep(uniform(0.1, 0.13))
            # print("6번째 :",time.time() - aa)
            page_soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.implicitly_wait(10)
            
            title = page_soup.find('div', class_='title').text.strip()

            # if title:
            #     title - title.text.strip()
                
            question = page_soup.find('div', class_='c-heading__content').text.strip()
            # if question:
            #     question = question.text.strip()

            answers = [ans.text.strip() for ans in page_soup.find_all('div', class_='_endContentsText c-heading-answer__content-user')]
            if len(answers) == 0:
                answers = [ans.text.strip() for ans in page_soup.find_all('div', class_='se-main-container')]
                
            # print("6번째 :",time.time() - aa)

            if answers:
                csv_writer.writerow([title, question, answers[0], link])
                for answer in answers[1:]:
                    csv_writer.writerow([title, question, answer])
            else:
                csv_writer.writerow([title, question, ""])
                
        driver.close()
            
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if csv_file is not None:
            csv_file.close()
        # driver.close()

def crawl_keyword(keyword, start_date, end_date, sort, number):    
    for page in range(1, dead_line):
        crawl_page(keyword, start_date, end_date, sort, page)
        # if page == dead_line:
        #     cnt += 1
        print()
        print("추가 생성된 파일 개수 :",number)
        print("현재 크롤링 중인 page :",page)
        print("현재 크롤링 중인 keyword :",keyword[:5] if keyword[5] != "" else keyword[:6])
        print("현재 진행 중인 기간",start_date,"~",end_date)
        print()            

def change_date(date1):
    year1 = int(date1[:4])
    month1 = int(date1[5:7])
    day1 = int(date1[-2:])
    
    day1 -= 5
    
    if day1 <= 0:
        day1 += 30
        month1 -= 1
        
        if month1 <= 0:
            month1 = 12
            year1 -= 1
    
    if len(str(month1)) == 2 and len(str(day1)) == 2:
        new_date = str(year1) + "." + str(month1) + "." + str(day1)
        
    elif len(str(month1)) == 1 and len(str(day1)) == 1:
        month1 = "0" + str(month1)
        day1 = "0" + str(day1)
        new_date = str(year1) + "." + str(month1) + "." + str(day1)
    
    elif len(str(month1)) == 1:
        month1 = "0" + str(month1)
        new_date = str(year1) + "." + str(month1) + "." + str(day1)
        
    elif len(str(day1)) == 1:
        day1 = "0" + str(day1)
        new_date = str(year1) + "." + str(month1) + "." + str(day1)
        
    return new_date 
        
def main(date1, date2, number):    
    if __name__ == "__main__":
        # print("프로그램을 시작합니다")
        keywords = ["어느 병원", "어떤 병원"]
        start_date = date1
        end_date = date2
        sort = 'date'
        # cnt = 0

        ensure_dir("output")

        processes = []
        for keyword in keywords:
            p = Process(target=crawl_keyword, args=(keyword + " -동물 -성형 -강아지 -피부과 -개인회생 -인테리어 -진로 -커리큘럼 -자동차 -도서 -보험 -교통 -차 -간호학과 -학과", start_date, end_date, sort, number))
            processes.append(p)
            p.start()
            
        for p in processes:
            p.join()

        start_date = change_date(start_date)
        end_date = change_date(end_date)
        number += 1
        
        main(start_date,end_date, number)
        
global dead_line, set_links

end_date = "2024.04.16"
start_date = "2024.04.12"

dead_line = 3

service = Service(ChromeDriverManager().install())

set_links = set()

main(start_date,end_date,1)
