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
import chromedriver_autoinstaller
from selenium.webdriver import ActionChains
## =======================================================================================
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--dns-prefetch-disable')
options.add_argument("start-maximized")
chrome_path = chromedriver_autoinstaller.install()
driver = webdriver.Chrome(chrome_path, options=options)
driver.implicitly_wait(2)

# 검색하고자 하는 웹사이트 입력
web_site = 'https://www.wconcept.co.kr/Product/301085943' # 검색하고자 하는 웹사이트 입력

driver.get(web_site) # 해당 웹사이트에 접속
time.sleep(1)  # 2초간 정지

# 몇개의 리뷰가 있는지 확인 -> 한 페이지에 6개 리뷰가 있으므로 몇페이지까지 이동해야 하는지 확인
review_cnt = driver.find_element_by_id('reviewCnt1').text
print('총 리뷰개수 : ', review_cnt)

# 리뷰를 보기 위한 페이지로 이동
driver.find_element_by_xpath('//*[@id="frmproduct"]/div[2]/p[3]').click()

# 빈 리스트 만들어서, 리뷰 크롤링 시작하기
review_list=[]
option_list=[]

for k in range(1, math.ceil(int(review_cnt)/6)+1): # 1 페이지에 6개의 리뷰가 있으므로, 리뷰총개수를 6으로 나눈만큼 반복문실행
    # 리뷰 가져오기
    for i in range(1,7):
        # 리뷰 가져오기
        try : 
            review = driver.find_element_by_xpath('//*[@id="reviewList"]/table/tbody/tr[{}]/td[2]/div[1]/p'.format(i)).text
            review_list.append(review)
        except:
            review_list.append('0')
        time.sleep(2)
        
        # 구매옵션 가져오기
        try :
            option = driver.find_element_by_xpath('//*[@id="reviewList"]/table/tbody/tr[{}]/td[2]/div[1]/div/div/div'.format(i)).text
            option_list.append(option)
        except : 
            option_list.append('0')        
    time.sleep(2)        
    
    # 페이지 이동을 클릭하기 전에 해당 페이지로 화면 이동
    action = ActionChains(driver)
    image_view = driver.find_element_by_xpath('//*[@id="qa"]') 
    action.move_to_element(image_view).perform()
    time.sleep(1.5)
    
    # 다음페이지로 이동
    k = k+1
    if (k % 11 == 0 ): 
        driver.find_element_by_xpath('//*[@id="reviewList"]/ul/li[13]/a').click()
    elif (k > 1) and (k % 11) != 0 :
        driver.find_element_by_xpath('//*[@id="reviewList"]/ul/li[{}]'.format(int((k%10)+2))).click()
    time.sleep(1.5)

driver.quit()

len(review_list)
len(option_list)

## 리뷰 크롤링 결과를 바탕으로 데이터 프레임으로 만들기
# 크롤링 저장 데이터를 DF로 생성
review_df = pd.DataFrame(zip(review_list, option_list), columns=['Review', 'Option'])
## 이 부분은 해당 상품명을 넣어주어야 함
review_df['Product_Name'] = 'ouie313 cotton collar knit' # 상품명 컬럼 생성
review_df.reset_index(inplace=True) # 고유 KEY로 활용하기 위한 index 컬럼추가

# option을 통해 추출한 값을 가공하여 추가 컬럼 만들기 (컬러옵션/사이즈)
review_df['Color'] = review_df['Option'].str.split(', ').str.get(0)

# 불필요한 컬럼 삭제
review_df.drop(['Option'], axis=1, inplace=True)

# 컬럼순서 변경
review_df.columns
review_df = review_df[['index','Product_Name',"Color","Review"]]

# 최종 파일을 csv 형식으로 변환
review_df.to_csv('Review_df_{}.csv'.format(review_df['Product_Name'][0]),encoding='utf-8-sig', index=False)

