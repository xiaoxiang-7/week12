from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>資訊管理導論作業</h1>"
    homepage += "<p>姓名：簡志翔</p>"
    homepage += "<p>系級：資管三B</p>"
    homepage += "<p>學號：410637340</p>"
    #homepage += "<a href=/account>網頁表單輸入實例</a><br><br>"
    homepage += "<a href=/search>電影查詢</a><br><br>"
    return homepage

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        cond = request.form["keyword"] #對應read.py第7行的cond代碼
        result = "您輸入的電影關鍵字是：" + cond
        
        db = firestore.client()
        collection_ref = db.collection("簡志翔電影")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if cond in dict["title"]:
                #print("{}老師開的{}課程,每週{}於{}上課".format(dict["Leacture"], dict["Course"],  dict["Time"],dict["Room"]))
                result += "片名：" + dict["title"] + "<br>"
                result += "電影介紹：" + dict["hyperlink"] + "<br><br>"

            if result =="":
                #如果查無資料，顯示以下錯誤訊息
                result = "抱歉，查無相關條件的電影資訊"

        #return result
    else:
        return render_template("search.html")

#if __name__ == "__main__":
#    app.run()