FROM continuumio/miniconda3


RUN conda install python=3.8
RUN conda install -c anaconda pymysql flask
RUN conda install -c conda-forge jieba flask-sqlalchemy flask-cors

COPY a01_flask.py .
COPY ntusd-negative.txt .
COPY ntusd-positive.txt .
ENV datebase_url=username:password@host.docker.internal:3306/jieba

ENV flask_port=8411
EXPOSE 8411

CMD ["python", "a01_flask.py"]
