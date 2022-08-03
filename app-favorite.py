from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.sx0y034.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta_project

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from datetime import datetime

#메인페이지
@app.route('/')
def home():
    return render_template('favorite.html')


# 메인페이지에서 즐찾 등록
@app.route("/bestseller", methods=["POST"])
def save_favorite():
    image_receive = request.form['image']
    title_receive = request.form['title']
    author_receive = request.form['author']
    userid_receive = request.form['userid']

    today = datetime.now()
    todaytime = today.strftime('%y-%m-%d')

    # favoritebooks_list = list(db.favoritebooks.find({}, {'_id': False}))
    # num = len(favoritebooks_list) + 1

    doc = {
        # 'num': num,
        'image':image_receive,
        'title': title_receive,
        'author': author_receive,
        'date': todaytime,
        'userid': userid_receive,
        'done':0,
        'saved':0
    }
    db.favoritebooks.insert_one(doc)
    return jsonify({'msg': '즐겨찾기 완료!'})


# 즐찾페이지 (클릭시)
@app.route('/favorite/list', methods=['GET'])
def show_favorite_page():
    userid = request.args.get('userid', type = str)
    return render_template('favorite.html',userid = userid)

# 즐찾페이지 조회시
@app.route('/api/favorite/list', methods=['GET'])
def show_favorite_book_list():
    userid=request.args.get('userid')
    bookName_list= list(db.favoritebooks.find({'saved':0,'userid':userid}, {'_id': False}))
    return jsonify({'favoritebooks': bookName_list})

# 리뷰등록->작성완료 read_done 포스트->목록에서 사라짐 saved=1
@app.route("/api/favorite/read_done", methods=["POST"])
def read_done():
    userid = request.form['userid']
    title_receive=request.form['title_give']
    db.favoritebooks.update_one({'userid':userid,'title':title_receive}, {'$set': {'done': 1}})
    return jsonify({'msg': '작성완료'})

# 즐찾 취소 unlike 포스트->목록에서 사라짐 saved=1
@app.route("/api/favorite/unlike", methods=["POST"])
def unlike():
    userid = request.form['userid']
    title_receive = request.form['title_unlike']
    db.favoritebooks.update_one({'userid': userid, 'title': title_receive}, {'$set': {'saved': 1}})
    return jsonify({'msg': '취소완료'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)