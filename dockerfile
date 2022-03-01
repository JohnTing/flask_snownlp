FROM continuumio/miniconda3


RUN conda install python=3.8

RUN conda install -c conda-forge snownlp jieba
RUN conda install flask pyinstaller 
RUN conda install -c anaconda pymysql 
RUN conda install -c conda-forge flask-sqlalchemy flask-cors

COPY a01_flask_snownlp.py .

ENV datebase_url=username:password@host.docker.internal:3306/snownlp

ENV flask_port=8401
EXPOSE 8401

CMD ["python", "a01_flask_snownlp.py"]
