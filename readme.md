# 建立 image
docker build . -t flask_jieba

# 環境設定
ENV datebase_url=mysql+pymysql://username:password@host.docker.internal:3306/database

# mysql 帳號，密碼，位置，資料庫
# 分別為 username password @host.docker.internal:3306 database

# 執行 image

docker run -d -p 8411:8411 -e datebase_url=sentiment:sentimentpassword@host.docker.internal:3306/sentiment -v C:\docker_ssl:/ssl flask_jieba

# 測試
https://localhost:8411/s?user_id=u測試&experiment_id=e測試&text=今天天氣不錯

