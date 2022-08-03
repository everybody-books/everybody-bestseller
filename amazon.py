from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

element_list = []

page_url = "https://www.amazon.com/Best-Sellers-Books/zgbs/books"
driver = webdriver.Chrome()
driver.get(page_url)

photo = driver.find_elements(By.XPATH, "//img[@class='a-dynamic-image p13n-sc-dynamic-image p13n-product-image']")
title = driver.find_elements(By.XPATH, "//a[@class='a-link-normal']//div[@class='_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y']")
# title = driver.find_elements(By.CLASS_NAME, "title")
author = driver.find_elements(By.XPATH, "//div[@class='a-row a-size-small']//div[@class='_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y']")
# review = driver.find_elements(By.XPATH, "//div[@class='ss_book_list']//ul/li[5]]")

# print(author)
# print(len(title))
# print(len(author))

for i in range(len(title)):
    element_list.append({"bookstore": "amazon", "rank": i+1, "title": title[i].text, "author": author[i].text, "photo": photo[i].get_attribute('src')})
    # element_list.append({"title": title[i].text, "author": author[i].text, "review": review[i].get_attribute('alt')})

print('수집 최종 형태: %s'%element_list)
print('랭킹 개수: %s'%len(element_list))

driver.quit()