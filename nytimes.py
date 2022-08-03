from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

element_list = []

page_url = "https://www.nytimes.com/books/best-sellers/combined-print-and-e-book-fiction/"
driver = webdriver.Chrome()
driver.get(page_url)

photo = driver.find_elements(By.XPATH, "//div[@class='css-szqx50']//a/img")
title = driver.find_elements(By.XPATH, "//h3[@class='css-5pe77f']")
# title = driver.find_elements(By.CLASS_NAME, "title")
author = driver.find_elements(By.XPATH, "//p[@itemprop='author']")
# review = driver.find_elements(By.XPATH, "//div[@class='ss_book_list']//ul/li[5]]")

# print(author)
# print(len(title))
# print(len(author))

for i in range(len(title)):
    element_list.append({"bookstore": "nytimes", "rank": i+1, "title": title[i].text, "author": author[i].text[3:], "photo": photo[i].get_attribute('src')})
    # element_list.append({"title": title[i].text, "author": author[i].text, "review": review[i].get_attribute('alt')})

print('수집 최종 형태: %s'%element_list)
print('랭킹 개수: %s'%len(element_list))

driver.quit()