from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

element_list = []

page_url = "http://www.yes24.com/24/Category/BestSeller"
driver = webdriver.Chrome()
driver.get(page_url)

photo = driver.find_elements(By.XPATH, "//p[@class='image']//img")
title = driver.find_elements(By.XPATH, "//p[contains(text(), '[도서]')] | //p[contains(text(), '[만화]')]")
author = driver.find_elements(By.XPATH, "//p[@class='aupu']")


print(len(photo))
print(len(title))
print(len(author))



# title = driver.find_elements(By.XPATH, "//div[@class='title' and string-length(text()) > 0]")
# author = driver.find_elements(By.XPATH, "//div[@class='aupu' and string-length(text()) > 0 and @class!='span']")
# review = driver.find_elements(By.XPATH, "//img[contains(@src, 'smallStar')]")


for i in range(len(title)):
    element_list.append({"bookstore": "예스24", "rank": i+1, "title": title[i].text, "author": author[i].text, "photo": photo[i].get_attribute('src')})
    # element_list.append({"title": title[i].text, "author": author[i].text, "review": review[i].get_attribute('alt')})

print('수집 최종 형태: %s'%element_list)
print('랭킹 개수: %s'%len(element_list))

driver.quit()