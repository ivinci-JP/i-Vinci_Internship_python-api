FROM python:3

RUN pip install requests

# アプリケーションディレクトリを作成する
WORKDIR /app

COPY . /app

EXPOSE 8000

CMD [ "python", "sample.py" ]