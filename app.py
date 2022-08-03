from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
from datetime import datetime

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.lz7xw.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

# 교보 크롤링
kyobo_list = []

page_url = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf"
driver = webdriver.Chrome()
driver.get(page_url)
image = driver.find_elements(By.XPATH, "//img[contains(@src, 'http://image.kyobobook.co.kr/images/book/large/')]")
title = driver.find_elements(By.XPATH, "//div[@class='title' and string-length(text()) > 0]")
title.pop(0)
auAndPu = driver.find_elements(By.XPATH, "//div[@class='author' and string-length(text()) > 0 and @class!='span']")

for i in range(0, 20):
    kyobo_list.append({"bookstore": "교보문고", "rank": i+1, "title": title[i].text, "author": auAndPu[i].text.split('|')[0].strip(), "publisher":auAndPu[i].text.split('|')[1].strip(), "image": image[i].get_attribute('src')})

driver.quit()

# 영풍 크롤링
yp_list = []

page_url = "https://www.ypbooks.co.kr/book_arrange.yp?targetpage=book_week_best&pagetype=5&depth=1"
driver = webdriver.Chrome()
driver.get(page_url)

image = driver.find_elements(By.XPATH, "//img[@class='thumb']")
title = driver.find_elements(By.XPATH, "//a[@class='boxiconset_bk_tt']")
auAndPu = driver.find_elements(By.XPATH, "//dd[@class='nbookName']")

for i in range(0, 20):
    yp_list.append({"bookstore": "영풍문고", "rank": i+1, "title": title[i].text, "author": auAndPu[i].text.split('|')[0].strip(), "publisher":auAndPu[i].text.split('|')[1].strip(), "image": image[i].get_attribute('src')})


driver.quit()

# yes24 크롤링
yes_list = []

page_url = "http://www.yes24.com/24/Category/BestSeller"
driver = webdriver.Chrome()
driver.get(page_url)

image = driver.find_elements(By.XPATH, "//p[@class='image']//img")
title = driver.find_elements(By.XPATH, "//p[contains(text(), '[도서]')] | //p[contains(text(), '[만화]')]")
auAndPu = driver.find_elements(By.XPATH, "//p[@class='aupu']")

for i in range(0, 20):
    yes_list.append({"bookstore": "예스24", "rank": i+1, "title": title[i].text,"author": auAndPu[i].text.split('|')[0].strip(), "publisher":auAndPu[i].text.split('|')[1].strip(), "image": image[i].get_attribute('src')})


driver.quit()

# 알라딘 크롤링

aladin_list = []

page_url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1"
driver = webdriver.Chrome()
driver.get(page_url)

image = driver.find_elements(By.XPATH, "//img[@class='front_cover'] | //img[@class='front_cover i_cover']")
title = driver.find_elements(By.XPATH, "//a[@class='bo3']")
auAndPu = driver.find_elements(By.XPATH, "//div[@class='ss_book_list']//li[descendant::a[contains(@href, 'AuthorSearch')]]")

for i in range(0, 20):
    aladin_list.append({"bookstore": "알라딘", "rank": i+1, "title": title[i].text, "author": auAndPu[i].text.split('|')[0].strip(), "publisher":auAndPu[i].text.split('|')[1].strip(), "image": image[i].get_attribute('src')})

driver.quit()
#
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/bestseller')
def bestseller():

    myname = 'sparta'
    return render_template("bestseller.html", name=myname, kyobo_list=kyobo_list, yp_list=yp_list, yes_list=yes_list, aladin_list=aladin_list)


@app.route('/review')
def review():
    return render_template('review.html')


@app.route("/getFavorite", methods=["POST"])
def get_favorite():
    name_receive = request.form['name_give']
    title_receive = request.form['title_give']
    author_receive = request.form['author_give']
    publisher_receive = request.form['publisher_give']
    image_receive = request.form['image_give']

    doc = {
        'username':name_receive,
        'title':title_receive,
        'author':author_receive,
        'publisher':publisher_receive,
        'image':image_receive
    }
    db.test.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/review/post", methods=["POST"])
def read_post():
    num_receive = request.form['num_give']
    star_receive = request.form['star_give']
    review_receive = request.form['review_give']
    date = datetime.today().strftime('%Y-%m-%d')
    db.favorites.update_one({'num': int(num_receive)}, {'$set': {'done': 1,'star':star_receive, 'review':review_receive, 'date':date, 'read':0}})

    return jsonify({'msg': '등록 완료!'})
#
@app.route("/review/cancel", methods=["POST"])
def cancel_read():
    num_receive = request.form['num_give']
    db.favorites.update_one({'num': int(num_receive)}, {'$set': {'read': 1}})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/review/list", methods=["GET"])
def review_get():
    read_list = list(db.favorites.find({'done':1}, {'_id': False}))
    return jsonify({'review': read_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)