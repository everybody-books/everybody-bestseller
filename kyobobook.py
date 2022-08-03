from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import urllib


element_list = []


# 셀레니움 드라이버 설정 후 베스트셀러 정보들을 추출하는 과정

page_url = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf"
driver = webdriver.Chrome()
driver.get(page_url)
photo = driver.find_elements(By.XPATH, "//img[contains(@src, 'http://image.kyobobook.co.kr/images/book/large/')]")
title = driver.find_elements(By.XPATH, "//div[@class='title' and string-length(text()) > 0]")
title.pop(0)
author = driver.find_elements(By.XPATH, "//div[@class='author' and string-length(text()) > 0 and @class!='span']")
review = driver.find_elements(By.XPATH, "//img[contains(@alt, '5점 만점에')]")

# print(len(photo))
# print(photo)


## 베스트셀러 정보 및 사진들을 저장하는 과정

for i in range(len(title)):
    element_list.append({"bookstore": "교보문고", "rank": i+1, "title": title[i].text, "author": author[i].text, "review": review[i].get_attribute('alt'), "photo": photo[i].get_attribute('src')})
    # urllib.request.urlretrieve(photo[i].get_attribute("src"), 'temp/%s.jpg'%title[i].text)

print(element_list)


## 셀레니움 드라이버 취소

driver.quit()


## 몽고DB에 저장하는 과정

connect = MongoClient('mongodb+srv://randomvisitor:visitorcopy@cluster0.dl5c8.mongodb.net/?retryWrites=true&w=majority')
db = connect.bestseller
db.book.insert_many(element_list)