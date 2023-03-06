
## =======================================================================================
## 필요한 라이브러리 실행
import os
import pandas as pd
pd.set_option('display.float_format', '{:.3f}'.format) # 소수점 셋째짜리까지 표현되도록 지정
pd.set_option('display.max_rows', 100) # 보여지는 max 행의 수 100으로 세팅
pd.set_option('display.max_columns', 50) # 보여지는 max 컬럼 수 50으로 세팅
pd.set_option('display.max_colwidth', 100) # 보여지는 컬럼내 글자수 100으로 세팅

import numpy as np  
import re  # 정규표현식
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

## =======================================================================================
## 드라이버 옵션 지정 및 검색하고자 하는 웹사이트 입력
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--dns-prefetch-disable')
options.add_argument("start-maximized")
chrome_path = chromedriver_autoinstaller.install()
driver = webdriver.Chrome(chrome_path, options=options)
driver.implicitly_wait(2)

# 검색하고자 하는 웹사이트 입력
web_site = 'https://www.musinsa.com/app/goods/2699766' # 검색하고자 하는 웹사이트 입력
## =======================================================================================


driver.get(web_site) # 크롬드라이버가 해당 웹사이트에 접속
time.sleep(1)  # 2초간 정지
general_size_review = driver.find_element_by_xpath('//*[@id="product_size_recommend"]/ul').text
brand = driver.find_element_by_xpath('//*[@id="page_product_detail"]/div[3]/div[3]/div[1]/p/a[3]').text
item_key = driver.find_element_by_xpath('//*[@id="page_product_detail"]/div[3]/div[3]/span/em').text # 상품명 정보
brand_key = driver.find_element_by_xpath('//*[@id="page_product_detail"]/div[3]/div[3]/div[1]/p/a[3]').text # 브랜드명 정보

common_size_review = general_size_review.split('[회원추천]')

# product_size_df 이름으로 공통 사이즈 리뷰에 대한 데이터프레임 만들기
product_size_df = pd.DataFrame()
product_size_df['Size_Review'] = common_size_review[1:]

## 구매자 Demo 정보 관련 컬럼 생성
product_size_df['Demo'] = product_size_df['Size_Review'].str.split("기준\n").str.get(0)
product_size_df['Sex'] = product_size_df['Demo'].str[2:4]
product_size_df['Height'] = product_size_df['Demo'].str[5:8]
product_size_df['Weight'] = product_size_df['Demo'].str[11:].str.split('kg').str.get(0)

## 구매 내역에 대한 컬럼 생성
product_size_df['Temp'] = product_size_df['Size_Review'].str.split("기준\n").str.get(1)
product_size_df['Feedback'] = product_size_df['Temp'].str.split(" ").str.get(0)


#### ★★★★ 사이즈 컬럼이 보이는 기준이 계속 바뀌기 때문에 아래 코드를 수정하면서 확인이 필요함!!
product_size_df['Temp']

product_size_df['Size'] = product_size_df['Temp'].str.split(" ").str.get(1)

product_size_df['Size'] = product_size_df['Temp'].str.split("[").str.get(1).str.split("[").str.get(0).str.split(" ").str.get(-1)

product_size_df.drop(['Demo', 'Temp'], axis=1, inplace=True) # 불필요한 컬럼은 제거

## item_key에 대한 컬럼 추가
product_size_df['Product'] = item_key

Size_Feedback_df = product_size_df[['Product', 'Sex', 'Height', 'Weight', 'Size', 'Feedback']]
Size_Feedback_df[['PRODUCT', 'SEX', 'HEIGHT', 'WEIGHT', 'SIZE', 'FEEDBACK']] = product_size_df[['Product', 'Sex', 'Height', 'Weight', 'Size', 'Feedback']]
Size_Feedback_df.drop(['Product', 'Sex', 'Height', 'Weight', 'Size', 'Feedback'], axis=1, inplace=True)

Size_Feedback_df['BRAND'] = brand_key
Size_Feedback_df['BRAND'] = Size_Feedback_df['BRAND'].str.replace('(',"").str.replace(')',"")
Size_Feedback_df = Size_Feedback_df[['BRAND', 'PRODUCT', 'SEX', 'HEIGHT', 'WEIGHT', 'SIZE', 'FEEDBACK']]

Size_Feedback_df.head(2)

print("※ 공통 사이즈 리뷰 크롤링 완료 ※")    



## =======================================================================================
### ★ 사이즈 평균 관련 크롤링 함수 (Common_Product_df)
def Common_Product_df():
    
    driver.get(web_site) # 크롬드라이버가 해당 웹사이트에 접속
    time.sleep(1)  # 2초간 정지
    general_size_review = driver.find_element_by_xpath('//*[@id="product_size_recommend"]/ul').text
    brand = driver.find_element_by_xpath('//*[@id="page_product_detail"]/div[3]/div[3]/div[1]/p/a[3]').text
    item_key = driver.find_element_by_xpath('//*[@id="page_product_detail"]/div[3]/div[3]/span/em').text # 상품명 정보
    brand_key = driver.find_element_by_xpath('//*[@id="page_product_detail"]/div[3]/div[3]/div[1]/p/a[3]').text # 브랜드명 정보
    
    common_size_review = general_size_review.split('[회원추천]')

    # product_size_df 이름으로 공통 사이즈 리뷰에 대한 데이터프레임 만들기
    product_size_df = pd.DataFrame()
    product_size_df['Size_Review'] = common_size_review[1:]

    ## 구매자 Demo 정보 관련 컬럼 생성
    product_size_df['Demo'] = product_size_df['Size_Review'].str.split("기준\n").str.get(0)
    product_size_df['Sex'] = product_size_df['Demo'].str[2:4]
    product_size_df['Height'] = product_size_df['Demo'].str[5:8]
    product_size_df['Weight'] = product_size_df['Demo'].str[11:].str.split('kg').str.get(0)

    ## 구매 내역에 대한 컬럼 생성
    product_size_df['Temp'] = product_size_df['Size_Review'].str.split("기준\n").str.get(1)
    product_size_df['Feedback'] = product_size_df['Temp'].str.split(" ").str.get(0)
    
    ## ★★ 사이즈 컬럼이 보이는 기준이 계속 바뀌기 때문에 아래 코드를 수정하면서 확인이 필요함!!
    product_size_df['Size'] = product_size_df['Temp'].str.split("[").str.get(1).str.split("[").str.get(0).str.split(" ").str.get(-1)
    product_size_df.drop(['Demo', 'Temp'], axis=1, inplace=True) # 불필요한 컬럼은 제거
    
    ## item_key에 대한 컬럼 추가
    product_size_df['Product'] = item_key
    
    global Size_Feedback_df
    Size_Feedback_df = product_size_df[['Product', 'Sex', 'Height', 'Weight', 'Size', 'Feedback']]
    Size_Feedback_df[['PRODUCT', 'SEX', 'HEIGHT', 'WEIGHT', 'SIZE', 'FEEDBACK']] = product_size_df[['Product', 'Sex', 'Height', 'Weight', 'Size', 'Feedback']]
    Size_Feedback_df.drop(['Product', 'Sex', 'Height', 'Weight', 'Size', 'Feedback'], axis=1, inplace=True)
    
    Size_Feedback_df['BRAND'] = brand_key
    Size_Feedback_df['BRAND'] = Size_Feedback_df['BRAND'].str.replace('(',"").str.replace(')',"")
    Size_Feedback_df = Size_Feedback_df[['BRAND', 'PRODUCT', 'SEX', 'HEIGHT', 'WEIGHT', 'SIZE', 'FEEDBACK']]
    
    print("※ 공통 사이즈 리뷰 크롤링 완료 ※")    

Common_Product_df()


## csv로 만들기 전에, 파일형식 확인
Size_Feedback_df.head()
Size_Feedback_df.shape
## =======================================================================================


## =======================================================================================
### ★ 리뷰 크롤링
## 1. 스타일 후기 리뷰 크롤링 함수 (Review_Photo_Crawling)
def Review_Style_Crawling():

    driver.get(web_site)
    time.sleep(1)  # 2초간 정지

    ## 상품별로 들어가는 정보(product_review_df)
    user_info_list = [] # 구매자정보 
    product_info_list = [] # 리뷰남긴상품정보 → 상품명에 컬러정보가 남아있는 경우 있음
    star_info_list = [] # 구매자 평점 → 추후 감정분석에 사용
    text_review_list = [] # 구매자 텍스트 리뷰 
    size_review_list = [] # 구매자 사이즈 리뷰 
    user_level_list = [] # 구매자 레벨
    review_date_list = [] # 리뷰를 남긴 날짜 정보
    color_list = [] # 구매한 컬러사이즈
        
    # 스타일 후기 리뷰수 크롤링
    total_review = driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[1]').text
    total_review = int(total_review.split(' ')[0])
    brand = driver.find_element_by_xpath('//*[@id="page_product_detail"]/div[3]/div[3]/div[1]/p/a[3]').text # 브랜드정보
    image = driver.find_element_by_css_selector('#bigimg').get_attribute('src') # 이미지url


    for k in range(1, int(total_review)+1) : # int(total_review)+1
        try:                 
            # 상품명 정보
            pro_info = driver.find_elements_by_css_selector('.review-goods-information__item')
            for pro in pro_info:
                try:
                    pro_text = pro.text
                    product_info_list.append(pro_text)
                except: 
                    product_info_list.append("0")
                        
            # 구매 컬러사이즈 정보
            color_info = driver.find_elements_by_css_selector('.review-goods-information__option-wrap')
            for color in color_info:
                try:
                    color_text = color.text
                    color_list.append(color_text)
                except: 
                    color_list.append("0")
                            
            # 구매자 정보
            profiles = driver.find_elements_by_css_selector(".review-profile__information")
            for profile in profiles : 
                try : 
                    profile_text = profile.text
                    user_info_list.append(profile_text)
                except : 
                    user_info_list.append("0")
                                                
            # 구매자평점 → 추후 감정분석활용
            star_info = driver.find_elements_by_css_selector('.review-list__rating__active')
            for i in range(len(star_info)):
                try : 
                    width = star_info[i].get_attribute('style')
                    percent_star = int(re.findall('\d+', width)[0])
                    percent_star = percent_star*0.05
                    star_info_list.append(percent_star)            
                except : star_info_list.append("0")
            time.sleep(1)     
                        
            # 구매자 텍스트 리뷰
            text_info = driver.find_elements_by_css_selector('.review-contents__text')
            for text in text_info:
                try : 
                    text_li = text.text
                    text_li = text_li.replace("\n","")
                    text_li = text_li.replace("\t","")
                    text_review_list.append(text_li)
                except : text_review_list.append("0")
            time.sleep(1)
                            
            # 구매자 레벨 
            level_info = driver.find_elements_by_class_name('review-profile__name')
            for level in level_info:
                try : 
                    level_text = level.text
                    user_level_list.append(level_text)
                except : user_level_list.append("0")
                
            # 리뷰를 남긴 날짜 (review_date_list)
            review_dates = driver.find_elements_by_class_name('review-profile__date')
            for review_date in review_dates:
                try : 
                    review_date_text = review_date.text
                    review_date_list.append(review_date_text)
                except : review_date_list.append("0")    
                               
            find_tag = driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[2]') # 리뷰 다음페이지 넘기는 곳으로 페이지 이동
            action = ActionChains(driver)
            action.move_to_element(find_tag).perform()
            time.sleep(1)
                        
            ## 리뷰페이지를 넘겨보기 위한 코드                    
            if int(k) % 5 == 0 :
                driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[2]/div/a[8]').click()
                time.sleep(1.5)
                        
            else :
                driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[2]/div/a[{}]'.format(int((k%5)+3))).click()
                time.sleep(1.5)    
        except : pass
        
    global style_result_df
    style_result_df = pd.DataFrame({'User_info':user_info_list,'Product' : product_info_list,'Star_review' : star_info_list, 'Text_Review' : text_review_list, 'Review_Date': review_date_list, "User_Level":user_level_list, "Color":color_list })
    style_result_df['Brand'] = brand    
    style_result_df['url'] = image # 상품 URL 추가
    style_result_df['Release_Date'] = style_result_df['url'].str.split('/').str[-3] # 상품 출시일 추가
    
    print('※스타일 후기 크롤링 완료※')
    return style_result_df
Review_Style_Crawling()

style_result_df.head()
style_result_df.shape

## =======================================================================================


## =======================================================================================
## 2. 상품후기 리뷰 크롤링 함수 (Review_Photo_Crawling)
def Review_Product_Crawling():
    
    driver.get(web_site)
    time.sleep(1)  # 2초간 정지
    
    # 상품후기 페이지로 가서 해당 정보 확인
    find_tag_1 = driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[1]')
    action = ActionChains(driver)
    action.move_to_element(find_tag_1).perform()
    time.sleep(.5)
    driver.find_element_by_xpath('//*[@id="estimate_photo"]').click() # 상품후기 클릭!
    time.sleep(.5)

    ## 상품별로 들어가는 정보(product_review_df)
    user_info_list = [] # 구매자정보
    product_info_list = [] # 리뷰남긴상품정보 → 상품명에 컬러정보가 남아있는 경우 있음 
    star_info_list = [] # 구매자 평점 → 추후 감정분석에 사용
    text_review_list = [] # 구매자 텍스트 리뷰 
    size_review_list = [] # 구매자 사이즈 리뷰
    review_date_list = [] # 리뷰를 남긴 날짜 정보     
    user_level_list = [] # 구매자 레벨
    color_list = [] # 구매한 컬러사이즈
        
    # 스타일 후기 리뷰수 크롤링
    total_review = driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[1]').text
    total_review = int(total_review.split(' ')[0])
    brand = driver.find_element_by_xpath('//*[@id="page_product_detail"]/div[3]/div[3]/div[1]/p/a[3]').text # 브랜드정보
    image = driver.find_element_by_css_selector('#bigimg').get_attribute('src') # 이미지url

    for k in range(1,int(total_review)+1) :
        try:
            # 상품명 정보                             
            pro_info = driver.find_elements_by_css_selector('.review-goods-information__item')
            for pro in pro_info:
                try:
                    pro_text = pro.text
                    product_info_list.append(pro_text)
                except: 
                    product_info_list.append("0")            
            
            # 구매 컬러사이즈 정보
            color_info = driver.find_elements_by_css_selector('.review-goods-information__option-wrap')
            for color in color_info:
                try:
                    color_text = color.text
                    color_list.append(color_text)
                except: 
                    color_list.append("0")
                            
            # 구매자 정보
            profiles = driver.find_elements_by_css_selector(".review-profile__information")
            for profile in profiles : 
                try : 
                    profile_text = profile.text
                    user_info_list.append(profile_text)
                except : 
                    user_info_list.append("0")
                                                
            # 구매자평점 → 추후 감정분석활용
            star_info = driver.find_elements_by_css_selector('.review-list__rating__active')
            for i in range(len(star_info)):
                try : 
                    width = star_info[i].get_attribute('style')
                    percent_star = int(re.findall('\d+', width)[0])
                    percent_star = percent_star*0.05
                    star_info_list.append(percent_star)            
                except : star_info_list.append("0")
            time.sleep(1)     
                        
            # 구매자 텍스트 리뷰
            text_info = driver.find_elements_by_css_selector('.review-contents__text')
            for text in text_info:
                try : 
                    text_li = text.text
                    text_li = text_li.replace("\n","")
                    text_li = text_li.replace("\t","")
                    text_review_list.append(text_li)
                except : text_review_list.append("0")
            time.sleep(1)
                            
            # 구매자 레벨 
            level_info = driver.find_elements_by_class_name('review-profile__name')
            for level in level_info:
                try : 
                    level_text = level.text
                    user_level_list.append(level_text)
                except : user_level_list.append("0")
                
            # 리뷰를 남긴 날짜 (review_date_list)
            review_dates = driver.find_elements_by_class_name('review-profile__date')
            for review_date in review_dates:
                try : 
                    review_date_text = review_date.text
                    review_date_list.append(review_date_text)
                except : review_date_list.append("0") 
                                
                
            find_tag = driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[2]') # 리뷰 다음페이지 넘기는 곳으로 페이지 이동
            action = ActionChains(driver)
            action.move_to_element(find_tag).perform()
            time.sleep(1)
                        
            ## 리뷰페이지를 넘겨보기 위한 코드                    
            if int(k) % 5 == 0 :
                driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[2]/div/a[8]').click()
                time.sleep(1.5)
                        
            else :
                driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[2]/div/a[{}]'.format(int((k%5)+3))).click()
                time.sleep(1.5)    
        except : pass
        
    global product_result_df
    product_result_df = pd.DataFrame({'User_info':user_info_list,'Product' : product_info_list,'Star_review' : star_info_list, 'Text_Review' : text_review_list, "Review_Date": review_date_list, "User_Level":user_level_list, "Color":color_list })
    product_result_df['Brand'] = brand 
    product_result_df['url'] = image # 상품 URL 추가
    product_result_df['Release_Date'] = product_result_df['url'].str.split('/').str[-3] # 상품 출시일 추가
    
    print('※상품 후기 크롤링 완료※')
    return product_result_df
Review_Product_Crawling()

product_result_df.head()
product_result_df.shape
## =======================================================================================


## =======================================================================================
## 3. 일반후기 리뷰 크롤링 함수 (Review_Photo_Crawling)
def Review_Common_Crawling():
    
    driver.get(web_site)
    time.sleep(1)  # 2초간 정지
    
    # 상품후기 페이지로 가서 해당 정보 확인
    find_tag_1 = driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[1]')
    action = ActionChains(driver)
    action.move_to_element(find_tag_1).perform()
    time.sleep(.5)
    driver.find_element_by_xpath('//*[@id="estimate_goods"]').click() # 일반후기 클릭!
    time.sleep(.5)

    ## 상품별로 들어가는 정보(product_review_df)
    user_info_list = [] # 구매자정보 
    product_info_list = []
    star_info_list = [] # 구매자 평점 → 추후 감정분석에 사용
    text_review_list = [] # 구매자 텍스트 리뷰 
    size_review_list = [] # 구매자 사이즈 리뷰 
    review_date_list = [] # 리뷰를 남긴 날짜 정보  
    user_level_list = [] # 구매자 레벨
    color_list = [] # 구매한 컬러사이즈
        
    # 일반 후기 리뷰수 크롤링
    total_review = driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[1]').text
    total_review = int(total_review.split(' ')[0])
    brand = driver.find_element_by_xpath('//*[@id="page_product_detail"]/div[3]/div[3]/div[1]/p/a[3]').text # 브랜드정보
    image = driver.find_element_by_css_selector('#bigimg').get_attribute('src') # 이미지url
    
    for k in range(1, int(total_review)+1) :         
        try: 
            # 상품명 정보                             
            pro_info = driver.find_elements_by_css_selector('.review-goods-information__item')
            for pro in pro_info:
                try:
                    pro_text = pro.text
                    product_info_list.append(pro_text)
                except: 
                    product_info_list.append("0")                
                                        
            # 구매 컬러사이즈 정보
            color_info = driver.find_elements_by_css_selector('.review-goods-information__option-wrap')
            for color in color_info:
                try:
                    color_text = color.text
                    color_list.append(color_text)
                except: 
                    color_list.append("0")
                            
            # 구매자 정보
            profiles = driver.find_elements_by_css_selector(".review-profile__information")
            for profile in profiles : 
                try : 
                    profile_text = profile.text
                    user_info_list.append(profile_text)
                except : 
                    user_info_list.append("0")
                                                
            # 구매자평점 → 추후 감정분석활용
            star_info = driver.find_elements_by_css_selector('.review-list__rating__active')
            for i in range(len(star_info)):
                try : 
                    width = star_info[i].get_attribute('style')
                    percent_star = int(re.findall('\d+', width)[0])
                    percent_star = percent_star*0.05
                    star_info_list.append(percent_star)            
                except : star_info_list.append("0")
            time.sleep(1)     
                        
            # 구매자 텍스트 리뷰
            text_info = driver.find_elements_by_css_selector('.review-contents__text')
            for text in text_info:
                try : 
                    text_li = text.text
                    text_li = text_li.replace("\n","")
                    text_li = text_li.replace("\t","")
                    text_review_list.append(text_li)
                except : text_review_list.append("0")
            time.sleep(1)
                            
            # 구매자 레벨 
            level_info = driver.find_elements_by_class_name('review-profile__name')
            for level in level_info:
                try : 
                    level_text = level.text
                    user_level_list.append(level_text)
                except : user_level_list.append("0")

            # 리뷰를 남긴 날짜 (review_date_list)
            review_dates = driver.find_elements_by_class_name('review-profile__date')
            for review_date in review_dates:
                try : 
                    review_date_text = review_date.text
                    review_date_list.append(review_date_text)
                except : review_date_list.append("0")                 
                
            find_tag = driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[2]') # 리뷰 다음페이지 넘기는 곳으로 페이지 이동
            action = ActionChains(driver)
            action.move_to_element(find_tag).perform()
            time.sleep(1)
                        
            ## 리뷰페이지를 넘겨보기 위한 코드                    
            if int(k) % 5 == 0 :
                driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[2]/div/a[8]').click()
                time.sleep(1.5)
                        
            else :
                driver.find_element_by_xpath('//*[@id="reviewListFragment"]/div[11]/div[2]/div/a[{}]'.format(int((k%5)+3))).click()
                time.sleep(1.5)    
        except : pass
        
    global common_result_df
    common_result_df = pd.DataFrame({'User_info':user_info_list,'Product':product_info_list,'Star_review' : star_info_list, 'Text_Review' : text_review_list, "Review_Date": review_date_list, "User_Level":user_level_list, "Color":color_list })
    common_result_df['Brand'] = brand 
    common_result_df['url'] = image # 상품 URL 추가
    common_result_df['Release_Date'] = common_result_df['url'].str.split('/').str[-3] # 상품 출시일 추가
        
    print('※일반 후기 크롤링 완료※')
    return common_result_df
Review_Common_Crawling()

common_result_df.head()
common_result_df.shape

driver.quit() ## 4. 리뷰 크롤링 완료하고 크롬드라이버 종료
## =======================================================================================


## =======================================================================================
### ★ 3개 리뷰 크롤링 결과를 1개의 df로 만들기!
## 크롤링 결과 확인
print("스타일 리뷰 : " + str(style_result_df.shape))
print("제품 리뷰 : " + str(product_result_df.shape))
print("일반 리뷰 : " + str(common_result_df.shape))

## 크롤링 결과에 대해서 3개 데이터 프레임 합치기
Review_df = pd.concat([style_result_df, product_result_df, common_result_df])

Review_df.tail(2)
print('전체 리뷰 크롤링 결과 : ' +str(Review_df.shape))

## =======================================================================================


## =======================================================================================
### 전체 크롤링 DF 전처리
## 1) 크롤링 날짜 추가 
import datetime
d_today = datetime.date.today()
d_today = d_today.strftime("%Y-%m-%d")
Review_df['Crawling_Date'] = d_today # 크롤링 날짜 추가

Review_df['Review_Date'] = Review_df['Review_Date'].str.replace('.','-')

# 리뷰 남긴 날짜에 대한 가공
Review_df['Review_Date'] = Review_df['Review_Date'].str.replace('일 전',"").str.replace('시간 전',"").str.replace('분 전',"")

date_list = pd.date_range('2022-10-16', periods=31) # → 이부분은 날짜를 바꿔주기!!
date_list = pd.to_datetime(date_list, format='%Y-%m-%d')

Review_df['Review_Date'] = Review_df['Review_Date'].astype('object')

for i in range(len(date_list)) : 
    Review_df.loc[Review_df['Review_Date'] == str(i),'Review_Date'] = date_list[i]

Review_df['Review_Date'] = Review_df['Review_Date'].astype('str')
Review_df['Review_Date'] = Review_df['Review_Date'].str[:10]

Review_df['Review_Date'] = Review_df['Review_Date'].astype('object')
Review_df['Review_Date'] = pd.to_datetime(Review_df['Review_Date'], format='%Y-%m-%d')

Review_df.loc[Review_df['Review_Date']=='40', 'Review_Date'] = '2022-10-12'

Review_df['YEAR_RV'] = Review_df['Review_Date'].dt.year # 리뷰 남긴 연도 컬럼 추가
Review_df['MONTH_RV'] = Review_df['Review_Date'].dt.month # 리뷰 남긴 달 컬럼 추가 

Review_df['Release_Date'] = pd.to_datetime(Review_df['Release_Date'], format='%Y-%m-%d')
# Review_df['Release_Date'] = pd.to_datetime(Review_df['Release_Date'], errors='coerce') # 출시일 컬럼을 datetime 타입으로 변환

# 출시일-리뷰남긴날짜 차이의 컬럼 (TIMELAG) 추가
Review_df['TIMELAG'] = Review_df['Review_Date'] - Review_df['Release_Date'] 

## 데이터 프레임 컬럼별 전처리
Review_df['User_info'] = Review_df['User_info'].str.replace('\n신고',"") # 프로필만 남기기
Review_df['User_info'] = Review_df['User_info'].str.replace('신고',"")

Review_df['Sex'] = Review_df['User_info'].str.split(",").str.get(0) # User_info에서 Sex,Height,Weight 값 추출
Review_df['Height'] = Review_df['User_info'].str.split(",").str.get(1)
Review_df['Weight'] = Review_df['User_info'].str.split(",").str.get(2)

Review_df['Level'] = Review_df['User_Level'].str[:4] # 구매레벨만 추출
Review_df['User_ID'] = Review_df['User_Level'].str[4:] # 구매자 ID만 추출

Review_df.drop(['User_info'], axis=1, inplace=True) # 불필요한 컬럼은 제거
Review_df.drop(['User_Level'], axis=1, inplace=True) # 불필요한 컬럼은 제거



## =======================================================================================
## 2) 구매 상품의 컬러 / 사이즈 / 옵션구매 내역 전처리
## ★★★★ 이 부분 부터는 상품별로 달라지므로, 이 부분에 대한 컬럼은 유동적으로 변경! ★★★★
'''기본적으로 Color1 / Color2 / Size1 / Size2 / AddSelling 컬럼이 필요!(DB 구조에 맞춰줘야 함)
   해당 value가 없을 경우 np.nan으로 값을 채움 '''

## 전체 리뷰데이터 훑어보기!
Review_df['Color'] # 어떤 정보가 크롤링 되었는지 확인
Review_df['Product'] # 상품명 옆에 컬러옵션이 나타나는 경우


Review_df['COLOR_1'] = Review_df['Color'].str.replace('\n구매',"").str.split('/').str.get(0).str.split(')').str.get(1)
Review_df['SIZE_1'] = Review_df['Color'].str.replace('\n구매',"").str.split('/').str.get(1).str.split('_').str.get(0)

# 대부분 이걸 적용
Review_df['SIZE_1'] = Review_df['Color'].str.replace('\n구매',"")# 구매컬러/사이즈 정보만 남기기

# 일부 브랜드는 아래 기준이 적용
Review_df['SIZE_1'] = Review_df['Color'].str.replace('\n구매',"").str.split('/').str.get(0).str.replace('티셔츠 ',"")
Review_df['SIZE_2'] = Review_df['Color'].str.replace('\n구매',"").str.split('/').str.get(1).str.replace('셔츠 ',"")

Review_df['COLOR_1'] = Review_df['Color'].str.replace('\n구매',"").str.split('/').str.get(0)
Review_df['SIZE_1'] = Review_df['Color'].str.replace('\n구매',"").str.split("/").str.get(1)

# 스파오 상품은 아래 내용이 적용
Review_df['COLOR_1'] = Review_df['Color'].str.replace('\n구매',"").str.split('/').str.get(0).str.split(']').str.get(1)
Review_df['SIZE_1'] = Review_df['Color'].str.replace('\n구매',"").str.split("/").str.get(1).str.split('[').str.get(0)


## 이번에는 여기!!
Review_df['SIZE_1'] = Review_df['Color'].str.replace('\n구매',"").str.split(' , ').str.get(0).str.split('/').str.get(0).str.split('[').str.get(0).str.strip()
Review_df['COLOR_1'] = Review_df['Color'].str.replace('\n구매',"").str.split(' , ').str.get(0).str.split('/').str.get(1)

Review_df['COLOR_2'] = Review_df['Color'].str.replace('\n구매',"").str.split(' , ').str.get(1).str.split('/').str.get(0)
Review_df['SIZE_2'] = Review_df['Color'].str.replace('\n구매',"").str.split(' , ').str.get(1).str.split('/').str.get(1).str.split('[').str.get(0).str.strip()


## 컬러/사이즈 부분 확인하고 아래 기준으로 추가 컬럼 생성
Review_df['COLOR_1'] = np.nan

Review_df['SIZE_2'] = np.nan
Review_df['COLOR_2'] = np.nan

Review_df['ADD_SELLING'] = np.nan
Review_df.drop(['Color'], axis=1, inplace=True) # 불필요한 컬럼은 제거


# 최종 데이터 확인
Review_df.head(2)


# 제품명에 대해서 제품명만 남기기
Review_df['Product'] = Review_df['Product'].str.split('\n').str.split(',').str.get(0)

Review_df['Product'] = Review_df['Product'].str.replace('\n구매',"").str.split('\n').str.get(0)
Review_df['Product'] = Review_df['Product'].str.replace('\n구매',"").str.split('\n').str.get(0)

Review_df['COLOR_1'] = Review_df['Product'].str.split(' ').str.get(-1)

## =======================================================================================


## =======================================================================================
## 최종 컬럼 정리
# 데이터 구조에 맞춰서 컬럼명 변경
Review_df = Review_df.rename(columns={'Star_review':'STAR_REVIEW','Text_Review':'TEXT_REVIEW','Review_Date':'REVIEW_DATE','Product':'PRODUCT_NAME','Brand':'BRAND','Release_Date':'RELEASE_DATE','Sex':'SEX','Height':'HEIGHT','Weight':'WEIGHT','Level':'LEVEL','User_ID':'USER_ID', 'url':'URL'})
Review_df.drop(columns=['Crawling_Date'], axis=1, inplace=True)


# 컬럼순서 변경
Review_df = Review_df[['BRAND','PRODUCT_NAME','RELEASE_DATE','LEVEL','USER_ID','SEX', 'HEIGHT','WEIGHT','TEXT_REVIEW','STAR_REVIEW','REVIEW_DATE','YEAR_RV','MONTH_RV','TIMELAG','COLOR_1','SIZE_1','SIZE_2','COLOR_2','ADD_SELLING','URL']]

## 리뷰 중복된 행은 제거하고, 최종 데이터 프레임 shape 및 정보에 대해서 확인
Review_df = Review_df.drop_duplicates(['TEXT_REVIEW'], keep='first' , ignore_index=True)

## 나이/키 컬럼에 대해서 구간값 넣기
Review_df['HEIGHT'] = Review_df['HEIGHT'].str.strip().str.replace('cm',"").str.replace('kg',"")
Review_df['WEIGHT'] = Review_df['WEIGHT'].str.strip().str.replace('kg',"").str.replace('cm',"")
Review_df[['HEIGHT','WEIGHT']] = Review_df[['HEIGHT','WEIGHT']].fillna('9999')

Review_df[['HEIGHT','WEIGHT']] = Review_df[['HEIGHT','WEIGHT']].astype('int') # 키와 몸무게 컬럼의 데이터타입을 정수로 변환

## ★★★ 문제가 있을 경우 아래 코드를 활용하여 오류값은 제거!
Review_df.loc[Review_df['HEIGHT'] == '70kg', : ]
Review_df = Review_df.drop([26316])
Review_df.shape

## 키값에 대해서 범위로 구분
Review_df['HEIGHT_RANGE'] = np.nan
Review_df.loc[Review_df["HEIGHT"] < 150, 'HEIGHT_RANGE'] = '~ 150'
Review_df.loc[(150 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 155), 'HEIGHT_RANGE'] = '150 ~ 155'
Review_df.loc[(156 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 160), 'HEIGHT_RANGE'] = '156 ~ 160'
Review_df.loc[(161 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 165), 'HEIGHT_RANGE'] = '161 ~ 165'
Review_df.loc[(166 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 170), 'HEIGHT_RANGE'] = '166 ~ 170'
Review_df.loc[(171 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 175), 'HEIGHT_RANGE'] = '171 ~ 175'
Review_df.loc[(176 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 180), 'HEIGHT_RANGE'] = '176 ~ 180'
Review_df.loc[(181 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 185), 'HEIGHT_RANGE'] = '181 ~ 185'
Review_df.loc[(186 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 190), 'HEIGHT_RANGE'] = '186 ~ 190'
Review_df.loc[(191 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 195), 'HEIGHT_RANGE'] = '191 ~ 195'
Review_df.loc[(196 <= Review_df.HEIGHT) & (Review_df.HEIGHT <= 200), 'HEIGHT_RANGE'] = '195 ~ 200'

Review_df['HEIGHT_RANGE'].value_counts(dropna=False)

## 몸무게값에 대해서 범위로 구분
Review_df['WEIGHT_RANGE'] = np.nan
Review_df.loc[(40 >= Review_df.WEIGHT), 'WEIGHT_RANGE'] = '~ 40 '
Review_df.loc[(41 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 45), 'WEIGHT_RANGE'] = '41 ~ 45'
Review_df.loc[(46 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 50), 'WEIGHT_RANGE'] = '46 ~ 50'
Review_df.loc[(51 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 55), 'WEIGHT_RANGE'] = '51 ~ 55'
Review_df.loc[(56 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 60), 'WEIGHT_RANGE'] = '56 ~ 60'
Review_df.loc[(61 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 65), 'WEIGHT_RANGE'] = '61 ~ 65'
Review_df.loc[(66 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 70), 'WEIGHT_RANGE'] = '66 ~ 70'

Review_df.loc[(71 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 75), 'WEIGHT_RANGE'] = '71 ~ 75'
Review_df.loc[(76 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 80), 'WEIGHT_RANGE'] = '71 ~ 75'

Review_df.loc[(81 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 85), 'WEIGHT_RANGE'] = '71 ~ 75'
Review_df.loc[(86 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 90), 'WEIGHT_RANGE'] = '86 ~ 90'

Review_df.loc[(91 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 95), 'WEIGHT_RANGE'] = '91 ~ 95'
Review_df.loc[(96 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 100), 'WEIGHT_RANGE'] = '96 ~ 100'

Review_df.loc[(101 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 105), 'WEIGHT_RANGE'] = '101 ~ 105'
Review_df.loc[(106 <= Review_df.WEIGHT) & (Review_df.WEIGHT <= 110), 'WEIGHT_RANGE'] = '106 ~ 110'
Review_df.loc[(111 <= Review_df.WEIGHT)& (Review_df.WEIGHT <= 200), 'WEIGHT_RANGE'] = '111 ~ '

Review_df['WEIGHT_RANGE'].value_counts(dropna=False)

## 나이/성별/키 컬럼의 null값(9999로 되어있는 값)에 대해서 미응답으로 컬럼값 채우기
Review_df.loc[Review_df['HEIGHT']==9999,'HEIGHT'] = "미응답"
Review_df.loc[Review_df['WEIGHT']==9999,'WEIGHT'] = "미응답"
Review_df['SEX'] = Review_df['SEX'].fillna('미응답') # 성별 컬럼 공백 처리


## 브랜드 컬럼의 특수문자 제거
Review_df['BRAND'] = Review_df['BRAND'].str.replace('(','').str.replace(')','')

Review_df.shape
Review_df.columns 
Review_df.tail(3) # 끝에까지 데이터가 잘 만들어졌는지 확인

## =======================================================================================
## 1) 크롤링 상품명으로 폴더 만들기
folder_name = Review_df['PRODUCT_NAME'][0].replace('/','')
os.mkdir(folder_name)

## 2) 최종 크롤링 파일을 각 폴더에 csv로 저장
# 구매사이즈 공통정보에 대해서 csv 저장
Size_Feedback_df.to_csv('{folder_name}/{file_name}_Size_Feedback_DF.csv'.format(folder_name=folder_name,file_name=Review_df['PRODUCT_NAME'][0].replace('/','')), encoding='utf-8-sig', index=False) 

# 리뷰 크롤링 결과에 대해서 csv로 저장
Review_df.to_csv('{folder_name}/{file_name}_Review_DF.csv'.format(folder_name=folder_name,file_name=Review_df['PRODUCT_NAME'][0].replace('/','')), encoding='utf-8-sig', index=False) 


