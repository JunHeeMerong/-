from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request as req
import time
driver = webdriver.Chrome()
url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query='
driver.get(url)
# driver.maximize_window() # 화면을 열고 풀스크린으로 적용
car_list = ['카니발','G80','그랜저','G90','GV80','K3','LF쏘나타','트레일블레이저','모하비','스파크','니로플러스',
            '코나','아반떼N','티볼리 에어','트래버스','볼트EUV','말리부','이쿼녹스','트랙스','볼트EV','타호','니로','르노 조에'
            ,'코나N','벨로스터N','코란도이모션','트위지']
for i in car_list:
    print('--------------------------------------------------------------------')
    print(i)
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, '#nx_query').send_keys(i + Keys.ENTER)
    time.sleep(1)
    infolist = driver.find_elements(by=By.TAG_NAME,value="dd")
    info = [i.text for i in infolist]
    # print(info)

    price = [i for i in info if i.find('만원')>0]
    price_index = price[0].index('만원')
    print('가격 : ',price[0][:price_index],'만원')
    fuel_efficiency = [i for i in info if i.find('km')>0]
    print('연비 : ',fuel_efficiency[0])
    index = info.index(fuel_efficiency[0])
    fuel = info[1:index]
    print('연료 : ',[i for i in fuel if i!=''])

    