from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

element_list = []

page_url = "https://www.ypbooks.co.kr/book_arrange.yp?targetpage=book_week_best&pagetype=5&depth=1"
driver = webdriver.Chrome()
driver.get(page_url)

photo = driver.find_elements(By.XPATH, "//img[@class='thumb']")
title = driver.find_elements(By.XPATH, "//a[@class='boxiconset_bk_tt']")
# title = driver.find_elements(By.CLASS_NAME, "title")
author = driver.find_elements(By.XPATH, "//dd[@class='nbookName']")
# review = driver.find_elements(By.XPATH, "//div[@class='ss_book_list']//ul/li[5]]")

# print(author)
# print(len(title))
# print(len(author))

for i in range(len(title)):
    element_list.append({"bookstore": "영풍문고", "rank": i+1, "title": title[i].text, "author": author[i].text, "photo": photo[i].get_attribute('src')})
    # element_list.append({"title": title[i].text, "author": author[i].text, "review": review[i].get_attribute('alt')})

print('수집 최종 형태: %s'%element_list)
print('랭킹 개수: %s'%len(element_list))

driver.quit()