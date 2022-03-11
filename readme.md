# 建立 image
docker build . -t flask_snownlp

# 環境設定
ENV datebase_url=mysql+pymysql://username:password@host.docker.internal:3306/database

# mysql 帳號，密碼，位置，資料庫
# 分別為 username password @host.docker.internal:3306 database

# 執行 image

docker run -d -p 8401:8401 -e datebase_url=sentiment:sentimentpassword@host.docker.internal:3306/sentiment -v C:\docker_ssl:/ssl flask_snownlp

# 測試
https://localhost:8401/s?user_id=u測試&experiment_id=e測試&text=今天天氣不錯

