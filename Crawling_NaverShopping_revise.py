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
web_site = 'https://smartstore.naver.com/bestyours/products/4519409886?NaPm=ct%3Dleqbfysg%7Cci%3D2fd3fd70e4c785baecd9ebaf5031ae97e46db369%7Ctr%3Dslsl%7Csn%3D225517%7Chk%3De7b2208b4ddf23e3fde07cf1204fe628fce37b8e' # 검색하고자 하는 웹사이트 입력
driver.get(web_site) # 해당 웹사이트에 접속
time.sleep(1)  # 2초간 정지

## 리뷰에 대한 정보를 확인하기 위해 해당 위치로 드라이버 이동
action = ActionChains(driver)
review_section = driver.find_element(By.CLASS_NAME, '_6MRaF2_W0o') 
action.move_to_element(review_section).perform()
time.sleep(1.5)
## =======================================================================================

## =======================================================================================
## 빈 리스트 만들어서, 리뷰 크롤링 시작하기
review_content_list = [] # 실제 리뷰를 가져오기 위한 list
star_list = [] # 평점정보를 가져오기 위한 리스트
size_list = [] # 쇼핑몰 정보를 가져오기 위한 list
review_date_list = [] # 리뷰를 남긴 날짜를 가져오기 위한 list
info_list = []

# 리뷰 페이지수(review_cnt) 에 맞춰서 반복문 돌리기
review_page = 17

for k in range(1, review_page+1 ): 
    ## 리뷰가 20개씩 쌓이기 때문에, 20번 반복문 돌리기
    for i in range(20):

        review_box = driver.find_elements(By.CLASS_NAME, '_2389dRohZq')[i]
        
        # 리뷰 내용 (review_content)
        try:
            review_content = review_box.find_element(By.CLASS_NAME, '_19SE1Dnqkf').text # 리뷰 
            review_content_list.append(review_content)
        except: 
            review_content_list.append("0")            
        time.sleep(1)

        # 평점정보 가져오기
        try:
            star = review_box.find_element(By.CLASS_NAME, '_15NU42F3kT').text # 평점 
            star_list.append(star)
        except: 
            star_list.append("0")


        ## 구매사이트 정보
        # try:
        #     size = review_box.find_element(By.CLASS_NAME, '_38yk3GGMZq').text # 사이즈정보  
        #     size_list.append(size)
        # except: 
        #     size_list.append("0")

            
        # 구매상세정보 (_14FigHP3K8)
        try:
            info = review_box.find_element(By.CLASS_NAME, '_14FigHP3K8').text # 구매상세정보
            info_list.append(info)
        except: 
            info_list.append("0")

        # 리뷰를 남긴 날짜
        try:
            review_date = review_box.find_elements(By.CLASS_NAME, '_3QDEeS6NLn')[1].text # 날짜
            review_date_list.append(review_date)
        except: 
            review_date_list.append("0")

    ## 리뷰 다음 페이지로 넘기기
    review_number = driver.find_element(By.CLASS_NAME, '_1HJarNZHiI._2UJrM31-Ry') #_1HJarNZHiI _2UJrM31-Ry
    
    if k <= 5:
        review_number.find_element(By.XPATH,'//*[@id="REVIEW"]/div/div[3]/div[2]/div/div/a[{}]'.format(int(k+6))).click()
    else : review_number.find_element(By.XPATH,'//*[@id="REVIEW"]/div/div[3]/div[2]/div/div/a[12]').click() 
        
# 크롤링 결과 값의 개수가 맞는지 확인
print(len(review_content_list), len(star_list), len(info_list), len(review_date_list))

driver.quit() # 크롬 드라이버 닫기

## =======================================================================================

## =======================================================================================
## 크롤링 결과를 기반으로 데이터 프레임 만들고, 전처리 필요한 부분은 처리하기
review_df = pd.DataFrame({'Review_Contents': review_content_list, 'Review_Star':star_list, 'Review_Info':info_list, 'Review_Date':review_date_list})
review_df.shape # 5개의 컬럼이 생성되어야 함
review_df.head()

# 평점컬럼에서 평점이라는 글자 삭제하고, 숫자만 남기기
review_df['Review_Star'] = review_df['Review_Star'].str.replace("평점","")
review_df['Review_Star']

# 리뷰 남긴 날짜 기준으로 년도/월/일 정보 가져오기
review_df['Review_Year'] = review_df['Review_Date'].str.split(".").str[0]
review_df['Review_Month'] = review_df['Review_Date'].str.split(".").str[1]
review_df['Review_Day'] = review_df['Review_Date'].str.split(".").str[2]

review_df['Review_Info'] 

# 리뷰 상세 정보 파씽
type_list = []
color_list = []
size_list = []

for i in range(0, review_df.shape[0]):    
    try : 
        types = review_df['Review_Info'].str.split(' / ')[int(i)][0]
        type_list.append(types)
    except : type_list.append(0)

    try :     
        colors = review_df['Review_Info'].str.split(' / ')[int(i)][1]
        color_list.append(colors)
    except : color_list.append(0)

    try :     
        size = review_df['Review_Info'].str.split(' / ')[int(i)][2]
        size_list.append(size)
    except : size_list.append(0)

review_df['Type'] = type_list
review_df['Type'] = review_df['Type'].str.split(': ').str.get(1)

review_df['Colors'] = color_list
review_df['Colors'] = review_df['Colors'].str.split(': ').str.get(1)

review_df['Size'] = size_list
review_df['Size'] = review_df['Size'].str.split('\n').str.get(0).str.split(': ').str.get(1).str.split('_').str.get(0)

review_df.drop(columns=['Review_Info'], inplace=True)

review_df.head(2)
review_df.shape # 최종 shape은 컬럼수가 7개가 되어야 함!

## =======================================================================================

product = '솔트워터키즈샌들'
review_df['Product_Name'] = product

review_df.to_csv('review_df_{}.csv'.format(review_df['Product_Name'][0]), index=False, encoding='utf-8-sig')


