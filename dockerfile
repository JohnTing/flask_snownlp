FROM continuumio/miniconda3


RUN conda create -n snownlp python=3.8
RUN activate snownlp
RUN conda install -c conda-forge snownlp jieba
RUN conda install flask pyinstaller 
RUN conda install -c anaconda pymysql 
RUN conda install -c conda-forge flask-sqlalchemy

COPY a01_flask_snownlp.py .


ENV datebase_url=mysql+pymysql://sentiment:sentimentpassword@host.docker.internal:3306/sentiment

ENV flask_port=8401
EXPOSE 8401

CMD ["python", "a01_flask_snownlp.py"]