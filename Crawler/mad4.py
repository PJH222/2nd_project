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
    global aa
    csv_file = None    
    try:
        aa = time.time()
        options = webdriver.ChromeOptions()
        
        # 진행 중인 크롬 화면을 확인 하고 싶으시면
        # 하기 두줄을 주석 표시 ("#") 하시면 됩니다.
        # options.headless = True
        options.add_argument('headless')
        
        #argument 설정 참조 링크 (https://beomi.github.io/2017/09/28/HowToMakeWebCrawler-Headless-Chrome/)
        options.add_argument('window-size=1920x1080')
        options.add_argument('--log-level=3') 
        options.add_argument('--disable-loging')
        options.add_argument("--disable-gpu")
        options.add_argument("lang-ko_KR")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        
        
        driver = webdriver.Chrome(service=service, options=options)
 
        tmp = keyword[:5] if keyword[5] != "" else keyword[:6]
        
        directory = f"output/{tmp.replace(' ', '_')}"
        ensure_dir(directory)
        
        filename = f"{directory}/kin_{start_date}_{end_date}.csv"
        mode = 'a' if os.path.exists(filename) else 'w'

        csv_file = open(filename, mode=mode ,newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        
        url = create_search_url(keyword, page, start_date, end_date, sort)
        
        if mode == 'w':
            # 첫 페이지의 링크를 답변 칼럼 옆에 추가
            csv_writer.writerow(['제목', '질문', '답변',url])
        
        driver.get(url)
        driver.implicitly_wait(1.5)
        time.sleep(uniform(0.5, 1))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.implicitly_wait(1.5)
        time.sleep(uniform(0.5, 1))

        links = [tag['href'] for tag in soup.find_all('a', class_="_nclicks:kin.txt _searchListTitleAnchor")]
            
        for link in links:
            
            if page >= 60:
                # 60 페이지 이후,
                # 이전에 접속했던 링크가 입력된 경우
                # 접속하지 않고 다음 링크로 넘어가기
                if link in visited_links:
                    continue
                visited_links.add(link)
            
            driver.get(link)
            driver.implicitly_wait(1.5)
            time.sleep(uniform(0.5, 1))
            page_soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.implicitly_wait(1.5)
            time.sleep(uniform(0.5, 1))
            
            title = "" if page_soup.find('div', class_='title') is None else page_soup.find('div', class_='title').text.strip()
            question = "" if page_soup.find('div', class_='c-heading__content') is None else page_soup.find('div', class_='c-heading__content').text.strip()
            answers = [ans.text.strip() for ans in page_soup.find_all('div', class_='_endContentsText c-heading-answer__content-user')]
            
            if len(answers) == 0:
                answers = [ans.text.strip() for ans in page_soup.find_all('div', class_='se-main-container')]
                
            if answers:
                csv_writer.writerow([title, question, answers[0]])
                for answer in answers[1:]:
                    csv_writer.writerow([title, question, answer])
            else:
                csv_writer.writerow([title, question, ""])
        else:
            # 소요 시간에 대한 정보를 보고 싶지 않은 경우
            # 하기 세 줄을 주석 처리 할 것
            print()
            print(round(time.time() - aa,3), "초 소요 (한 페이지 크롤링 소요시간)")
            print("완료 시각 :",datetime.datetime.now())

            
            pass # 주석 처리하면 실행 안되니 유의할 것
        
        driver.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if csv_file is not None:
            csv_file.close()
        # driver.close()
        
def crawl_keyword(keyword, start_date, end_date, sort, number):
    global bb
    bb = time.time()   
    for page in range(1, dead_line):
        crawl_page(keyword, start_date, end_date, sort, page)
        print()
        print("추가 생성된 파일 개수 :",number)
        print("현재 크롤링 중인 page :",page)
        print("현재 크롤링 중인 keyword :",keyword[:5] if keyword[5] != "" else keyword[:6])
        print("현재 진행 중인 기간",start_date,"~",end_date,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print()
    # 소요 시간에 대한 정보를 보고 싶지 않은 경우
    # 하기 네 줄을 주석 처리 할 것
    tmp = dead_line - 1
    print()
    print(round(time.time() - bb,4), f"초 소요 ({tmp} 페이지 크롤링 소요시간)")
    print("완료 시각 :",datetime.datetime.now())
    
    
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
        # keywords 내에 키워드를 2개 넣으면 멀티 프로세싱으로
        # 두 가지 키워드를 동시에 크롤링 합니다. (이전에 vscode 두개 켜서 하는 것과 같습니다.)
        # 실행 시 컴퓨터가 버벅거린다 싶으시면 코드를 하나만 넣으시면 됩니다.
        # keywords = ["어느 병원"] << 이런 식으로
        keywords = ["어느 병원", "어떤 병원"]
        start_date = date1
        end_date = date2
        sort = 'date'

        ensure_dir("output")

        processes = []
        for keyword in keywords:
            # 제외 키워드를 추가하고 싶으시다면
            # 아랫줄 " -동물 -성형 -강아지 -피부과 -개인회생 -인테리어 -진로 -커리큘럼 -자동차 -도서 -보험 -교통 -차 -간호학과 -학과" 내에 기입하여 주시면 됩니다.
            p = Process(target=crawl_keyword, args=(keyword + " -동물 -성형 -강아지 -피부과 -개인회생 -인테리어 -진로 -커리큘럼 -자동차 -도서 -보험 -교통 -차 -간호학과 -학과", start_date, end_date, sort, number))
            processes.append(p)
            p.start()
            
        for p in processes:
            p.join()

        start_date = change_date(start_date)
        end_date = change_date(end_date)
        number += 1
        
        main(start_date,end_date, number)
        
# 5일 간격 기준으로 파일이 형성되도록 세팅 되어 있습니다.
easy_split = "2017.11.17 ~ 2017.11.21"

start_date = easy_split[:10]
end_date = easy_split[13:]

# 현재 진행 중인 기간 2017.11.17 ~ 2017.11.21   



global dead_line
dead_line = 89 # 몇 페이지까지 수집할 것인지 넣으시면 됩니다.

service = Service(ChromeDriverManager().install())

main(start_date,end_date,1)



# 2018.03.02 ~ 2018.03.06
