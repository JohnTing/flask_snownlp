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

from flask_cors import CORS

import os

datebase_url = "mysql+pymysql://" + os.environ.get("datebase_url", "username:password@host.docker.internal:3306/snownlp")
flask_port = int(os.environ.get("flask_port", 8401))

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = datebase_url
CORS(app)
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
        request_json = request.args
        text = request_json.get("text", "")
        user_id = request_json.get("user_id", "")
        experiment_id = request_json.get("experiment_id", "")

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


context = ('ssl/certificate.crt', 'ssl/private.key')

if __name__ == "__main__":
    
    if os.path.isfile(context[0]) and os.path.isfile(context[1]):
        print("use %s and %s as ssl." % (context[0], context[1]))
        app.run(debug=False, host="0.0.0.0", port=flask_port, ssl_context=context)
    else:
        print("ssl file no found, use http.")
        app.run(debug=False, host="0.0.0.0", port=flask_port)
    
