#!python
# conda create -n snownlp python=3.8
# conda install -c conda-forge snownlp jieba
# conda install flask pyinstaller
# conda install pyMySQLdb
# conda install -c anaconda pymysql


from ast import arg
from flask import Flask, jsonify, request
from snownlp import SnowNLP
import jieba
from flask_sqlalchemy import SQLAlchemy

import os


datebase_url = os.environ.get("datebase_url", "mysql+pymysql://sentiment:sentimentpassword@host.docker.internal:3306/sentiment")
flask_port = int(os.environ.get("flask_port", 8401))



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = datebase_url
db = SQLAlchemy(app)


class Sentiments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=True)
    experiment_id = db.Column(db.String(64), nullable=True)
    sentiment = db.Column(db.Float, nullable=True)
    text = db.Column(db.String(128), nullable=True)
    words = db.Column(db.String(128), nullable=True)

db.create_all()



@app.route("/sentiment", methods=['GET', 'POST'])
@app.route("/s", methods=['GET', 'POST'])
def hello_world():
    text = None
    user_id = None
    experiment_id = None

    if request.method == 'POST':
        request_json  = request.get_json()
        text = request_json.get("text", "")
        user_id = request_json.get("user_id", "")
        experiment_id = request_json.get("experiment_id", "")

    else:
        text = request.args.get("text", "")
        user_id = request.args.get("user_id", "")
        experiment_id = request.args.get(experiment_id, "")


    if text and len(text) > 0:
        result = getSentiment(text)
        sentiment = result.get("sentiment", -1)
        words = result.get("words", "")
        
        resultdb = Sentiments(experiment_id=experiment_id, 
                                user_id=user_id, 
                                sentiment=sentiment, text=text,words=("|".join(words)))

        db.session.add(resultdb)
        db.session.commit()
        return jsonify(result)
    else:
        return jsonify({"error", "no text."})

def getSentiment(text):    
    s = SnowNLP(text)
    seg_list = list(jieba.cut(text, cut_all=False))
    return {"sentiment": s.sentiments, "words":seg_list}

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=flask_port)