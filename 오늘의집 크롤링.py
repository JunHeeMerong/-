from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
noopen = webdriver.ChromeOptions()
# noopen.add_argument("headless")
driver = webdriver.Chrome(options=noopen)
# driver.maximize_window()
url = 'https://ohou.se/contents/card_collections?order=best'
driver.get(url)
time.sleep(2)
hreflist = []
scroll = 500
while len(hreflist)<500:
    imgcount = driver.find_elements(by=By.CLASS_NAME,value="card-collection-item__content__link")
    hreflist += [i.get_attribute("href") for i in imgcount if i.get_attribute("href") not in hreflist]
    driver.execute_script("window.scrollTo(0, {})".format(scroll))
    time.sleep(1)
    scroll+=500
print('총 '+str(len(hreflist))+'개')
count = 1
todayhome = pd.DataFrame(columns=['조회수','가구수','팔로워','댓글','좋아요','스크랩','공유','기타정보','해시태그'])
for url in hreflist:
    print('--------------------------------------------------------------------------------------------------')
    print(str(len(hreflist))+'개 중에 {}번'.format(count))
    driver.get(url)
    time.sleep(1)
    follow = driver.find_element(by=By.CLASS_NAME,value="css-18fcvol.e1y3nubp7")
    follow.click()
    time.sleep(1)
    fOllownumber = driver.find_element(by=By.CLASS_NAME,value="css-d2ibel.e1iro1t95")
    followcount = fOllownumber.text
    print('팔로워수 : ',followcount)
    followcount = followcount.replace(',','')
    driver.back()
    time.sleep(1)
    counting = driver.find_elements(by=By.TAG_NAME,value="dd")
    heart = driver.find_elements(by=By.CLASS_NAME,value="css-6emd9x.ei5bss2")
    thing = driver.find_elements(by=By.CLASS_NAME,value='css-q8kalz.e5rozk60')
    info = driver.find_elements(by=By.CLASS_NAME,value="css-eavncv.e15ygawh3")
    hashtag = driver.find_elements(by=By.CLASS_NAME,value='css-1cyj3hz.e1ls39b50')
    a = counting[0].text
    a = a.replace(',','')
    b = counting[1].text
    b = b.replace(',','')
    c = [i.text for i in heart][0]
    c = c.replace(',','')
    d = [i.text for i in heart][1]
    d = d.replace(',','')
    e = [i.text for i in heart][-1]
    e = e.replace(',','')
    todayhome.loc[count-1] = [int(a),len(thing),int(followcount),int(b),int(c),int(d),int(e),[i.text for i in info],[i.text for i in hashtag]]
    print('조회수 : ',counting[0].text,' '+'댓글수 : ',counting[1].text)
    print('좋아요 : ',[i.text for i in heart][0],'스크랩 : ',[i.text for i in heart][1],'공유 : ',[i.text for i in heart][-1])
    print('가구수 : ',len(thing))
    print('기타정보 : ',[i.text for i in info])
    print('해시태그 : ',[i.text for i in hashtag])
    count+=1
todayhome.to_csv("오늘의집 데이터.csv")