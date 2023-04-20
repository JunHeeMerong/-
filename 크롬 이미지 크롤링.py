import sys
import os
import urllib.request
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = Options()
chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
def doScrollDown(whileSeconds, driver):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break
    try:
        driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input').click()
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
    except:
        pass
header_n = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
def crawl(keywords, pages):
    path = "https://www.google.com/search?q=" + keywords + "&tbm=isch&ved=2ahUKEwj45vn1g9b5AhUFIIgKHVTtB1IQ2-cCegQIABAA&oq=" + keywords + "&gs_lcp=CgNpbWcQAzIECAAQQzIFCAAQgAQyBAgAEEMyBQgAEIAEMgUIABCABDIECAAQQzIECAAQQzIFCAAQgAQyBAgAEEMyBQgAEIAEOgQIIxAnOggIABCABBCxA1DqC1iYJ2CkN2gBcAB4AIAB0AGIAesFkgEFMC41LjGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=hCUBY_iUNIXAoATU2p-QBQ&bih=838&biw=1095"
    # 그냥 이것을 계속 사용하자
    # driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver') # selenium 3.x 버전용
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # selenium 4.x
    driver.implicitly_wait(3)
    driver.get(path)
    driver.maximize_window()
    time.sleep(1)
#    doScrollDown(60, driver) # 계속 읽어온다. 현재 1초에 한번씩 읽어오니까 60번...
    doScrollDown(pages, driver)   # 테스트: 계속 읽어온다. 현재 1초에 한번씩 읽어오니까 번
    time.sleep(1)       # 약간 여유를 준다.
    counter = 0
    succounter = 0
    print(os.path)
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/' + keywords):
        os.mkdir('data/' + keywords)
    # for x in driver.find_elements_by_class_name('rg_i.Q4LuWd'): # selenium 3.x 용
    for x in driver.find_elements(by=By.CLASS_NAME, value='rg_i.Q4LuWd'): #selenium 4.x 용
        counter = counter + 1
        print(counter)
        # 이미지 url
        img = x.get_attribute("data-src")
        if img is None:
            img = x.get_attribute("src")
        print(img)
        # 이미지 확장자
        imgtype = 'png'
        # 구글 이미지를 읽고 저장한다.
        try:
            raw_img = urllib.request.urlopen(img).read()
            File = open(os.path.join('data/' + keywords, keywords + "_" + str(counter) + "." + imgtype), "wb")
            File.write(raw_img)
            File.close()
            succounter = succounter + 1
        except:
            print('error')
    print(succounter, "succesfully downloaded")
    driver.close()
#crawl("strawberry", 5)  # 검색어, 페이지수(한페이지에 약 80 images)
crawl("Equinox car", 10)
print("끝")