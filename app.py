from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import urllib
import jwt
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.lz7xw.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta



app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


# 교보 크롤링
kyobo_list = []

page_url = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf"
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(chrome_options=chrome_options)
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
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(chrome_options=chrome_options)
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
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(chrome_options=chrome_options)
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
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(page_url)

image = driver.find_elements(By.XPATH, "//img[@class='front_cover'] | //img[@class='front_cover i_cover']")
title = driver.find_elements(By.XPATH, "//a[@class='bo3']")
auAndPu = driver.find_elements(By.XPATH, "//div[@class='ss_book_list']//li[descendant::a[contains(@href, 'AuthorSearch')]]")

for i in range(0, 20):
    aladin_list.append({"bookstore": "알라딘", "rank": i+1, "title": title[i].text, "author": auAndPu[i].text.split('|')[0].strip(), "publisher":auAndPu[i].text.split('|')[1].strip(), "image": image[i].get_attribute('src')})

driver.quit()

@app.route('/')
def main():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', name=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/bestseller')
def bestseller():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('bestseller.html', name=user_info, kyobo_list=kyobo_list, yp_list=yp_list, yes_list=yes_list, aladin_list=aladin_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
        return render_template("login.html")

@app.route('/review')
def show_review_page():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('review.html', name=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
        return render_template("login.html")

@app.route("/getFavorite", methods=["POST"])
def get_favorite():
    name_receive = request.form['name_give']
    title_receive = request.form['title_give']
    author_receive = request.form['author_give']
    publisher_receive = request.form['publisher_give']
    image_receive = request.form['image_give']
    date = datetime.today().strftime('%Y-%m-%d')

    doc = {
        'username':name_receive,
        'title':title_receive,
        'author':author_receive,
        'publisher':publisher_receive,
        'image':image_receive,
        'saved':0,
        'done':0,
        'date':date
    }
    db.favorites.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route('/favorite')
def show_favorite_page():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('favorite.html', name=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
        return render_template("login.html")

@app.route('/favorite/list', methods=['GET'])
def show_favorite_book_list():
    bookName_list= list(db.favorites.find({'saved':0}, {'_id': False}))
    return jsonify({'favoritebooks': bookName_list})

@app.route("/favorite/unlike", methods=["POST"])
def unlike():
    userid = request.form['userid']
    title_receive = request.form['title_unlike']
    db.favorites.update_one({'username': userid, 'title': title_receive}, {'$set': {'saved': 1}})
    return jsonify({'msg': '취소완료'})

@app.route("/favorite/post", methods=["POST"])
def read_post():
    star_receive = request.form['star_give']
    review_receive = request.form['review_give']
    date = datetime.today().strftime('%Y-%m-%d')
    userid = request.form['userid']
    title_receive=request.form['title_give']
    db.favorites.update_one({'username':userid,'title':title_receive}, {'$set': {'done': 1,'star':star_receive, 'review':review_receive, 'date':date, 'read':0}})
    return jsonify({'msg': '등록 완료!'})
#
@app.route("/review/cancel", methods=["POST"])
def cancel_read():
    userid = request.form['userid']
    title_receive = request.form['title_give']
    db.favorites.update_one({'username':userid,'title':title_receive}, {'$set': {'read': 1}})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/review/list", methods=["GET"])
def review_get():
    read_list = list(db.favorites.find({'done':1}, {'_id': False}))
    return jsonify({'review': read_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)