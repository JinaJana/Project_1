## 필요한 라이브러리 실행
import os
import pandas as pd
pd.set_option('display.float_format', '{:.3f}'.format) # 소수점 셋째짜리까지 표현되도록 지정
pd.set_option('display.max_rows', 100) # 보여지는 max 행의 수 100으로 세팅
pd.set_option('display.max_columns', 50) # 보여지는 max 컬럼 수 50으로 세팅
pd.set_option('display.max_colwidth', 100) # 보여지는 컬럼내 글자수 100으로 세팅
import numpy as np  
import re  # 정규표현식
import math
import time
import datetime
import warnings
warnings.filterwarnings('ignore')
import requests 
from bs4 import BeautifulSoup    # html 데이터를 전처리
from selenium import webdriver   # 웹 브라우저 자동화
from selenium.webdriver.common.keys import Keys # 브라우저에 입력
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver import ActionChains
## =======================================================================================

## =======================================================================================
## 크롬드라이버 실행
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--dns-prefetch-disable')
options.add_argument("start-maximized")
chrome_path = chromedriver_autoinstaller.install()
driver = webdriver.Chrome(chrome_path, options=options)
driver.implicitly_wait(2)

## 검색하고자 하는 웹사이트 입력
web_site = 'https://search.shopping.naver.com/catalog/28642954160?query=%EC%95%84%EB%8F%99%EC%83%8C%EB%93%A4&NaPm=ct%3Dleqbfn7s%7Cci%3D1d0d369db2f452baeb7a3485f0bbd79a1e66a299%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3Da575af52f621b8ef5bbc3f147eda3177a0d82a5d' # 검색하고자 하는 웹사이트 입력
#'https://search.shopping.naver.com/catalog/29051136654?query=%EC%95%84%EB%8F%99%20%ED%8C%A8%EB%94%A9&NaPm=ct%3Dlcr8gj48%7Cci%3De837bf74896779cdeecf321d074652f8bbecdcd7%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D8d2908db066fb7be8b96833838f4607024f067d5'

driver.get(web_site) # 해당 웹사이트에 접속
time.sleep(1)  # 2초간 정지

## 리뷰에 대한 정보를 확인하기 위해 해당 위치로 드라이버 이동
action = ActionChains(driver)
review_section = driver.find_element(By.CLASS_NAME, 'totalArea_graph_area__TUr84') 
action.move_to_element(review_section).perform()
time.sleep(1.5)

## 해당 상품에 대해서 몇 개의 리뷰가 있는지 확인 -> 한 페이지에 6개 리뷰가 있으므로 몇페이지까지 이동해야 하는지 확인
review_cnt = driver.find_elements(By.CLASS_NAME, 'totalArea_value__VV7TJ')[1].text
review_cnt = review_cnt.replace(',','') # 리뷰에 콤마는 삭제
print('총 리뷰개수 : ', review_cnt)
## =======================================================================================

## =======================================================================================
## 빈 리스트 만들어서, 리뷰 크롤링 시작하기
review_title_list = [] # 리뷰의 제목을 가져오기 위한 list 
review_content_list = [] # 실제 리뷰를 가져오기 위한 list
star_list = [] # 평점정보를 가져오기 위한 리스트
site_list = [] # 쇼핑몰 정보를 가져오기 위한 list
review_date_list = [] # 리뷰를 남긴 날짜를 가져오기 위한 list

review_page = 50

# 리뷰 페이지수(review_cnt) 에 맞춰서 반복문 돌리기
review_page = int(review_cnt)

for k in range(1, review_page+1 ): 
    ## 리뷰가 20개씩 쌓이기 때문에, 20번 반복문 돌리기
    for i in range(20):
        # 리뷰 제목 (review_title)
        try:
            review_title = driver.find_elements(By.CLASS_NAME, 'reviewItems_title__AwHcz')[i].text 
            review_title_list.append(review_title)
        except: 
            review_title_list.append("0")
        
        time.sleep(1)

        # 리뷰 내용 (review_content)
        try:
            review_content = driver.find_elements(By.CLASS_NAME, 'reviewItems_text__XrSSf')[i].text 
            review_content_list.append(review_content)
        except: 
            review_content_list.append("0")
            
        time.sleep(1)
        ## 평점 / 구매쇼핑몰 / 구매일자에 대한 정보
        review_info = driver.find_elements(By.CLASS_NAME, 'reviewItems_etc_area__3VUjt') 

        # 평점정보 가져오기
        try:
            star = review_info[i].find_elements(By.CLASS_NAME, 'reviewItems_average__0kLWX')[0].text 
            star_list.append(star)
        except: 
            star_list.append("0")

        # 구매사이트 정보
        try:
            site = review_info[i].find_elements(By.CLASS_NAME, 'reviewItems_etc__9ej69')[0].text  
            site_list.append(site)
        except: 
            site_list.append("0")

        # 리뷰를 남긴 날짜
        try:
            review_date = review_info[i].find_elements(By.CLASS_NAME, 'reviewItems_etc__9ej69')[2].text 
            review_date_list.append(review_date)
        except: 
            review_date_list.append("0")

    ## 리뷰 다음 페이지로 넘기기
    if k <= 10 :
        driver.find_element(By.XPATH, '//*[@id="section_review"]/div[3]/a[{}]'.format(int(k + 1))).click()               
    elif (k > 10) and (k % 10 == 9) : 
        driver.find_element(By.XPATH, '//*[@id="section_review"]/div[3]/a[{}]'.format(int((k+1)%10 + 11))).click()
    elif (k > 10) and (k % 10 == 0) : 
        driver.find_element(By.XPATH, '//*[@id="section_review"]/div[3]/a[{}]'.format(int((k+1)%10 + 11))).click()        
    else : 
        driver.find_element(By.XPATH, '//*[@id="section_review"]/div[3]/a[{}]'.format(int((k+1)%10 + 1))).click()        
    time.sleep(1)


# 크롤링 결과 값의 개수가 맞는지 확인
print(len(review_title_list),len(review_content_list), len(star_list), len(site_list), len(review_date_list))

driver.quit() # 크롬 드라이버 닫기

## =======================================================================================


## =======================================================================================
## 크롤링 결과를 기반으로 데이터 프레임 만들고, 전처리 필요한 부분은 처리하기
review_df = pd.DataFrame({'Review_Title':review_title_list, 'Review_Contents': review_content_list, 'Review_Star':star_list, 'Review_Site':site_list, 'Review_Date':review_date_list})
review_df.shape # 5개의 컬럼이 생성되어야 함
review_df.head()

# 평점컬럼에서 평점이라는 글자 삭제하고, 숫자만 남기기
review_df['Review_Star'] = review_df['Review_Star'].str.replace("평점","")
review_df['Review_Star']

# 리뷰 남긴 날짜 기준으로 년도/월/일 정보 가져오기
review_df['Review_Year'] = review_df['Review_Date'].str.split(".").str[0]
review_df['Review_Month'] = review_df['Review_Date'].str.split(".").str[1]
review_df['Review_Day'] = review_df['Review_Date'].str.split(".").str[2]

review_df.head(2)
review_df.shape # 최종 shape은 컬럼수가 8개가 되어야 함!

## =======================================================================================

review_df.to_csv('review_df_아디다스아달렛샌들.csv', index=False, encoding='utf-8-sig')


