FROM python:3.11-alpine3.17

WORKDIR /app
COPY . ./

RUN pip install -U pip wheel setuptools && pip install -Ur requirements.txt

EXPOSE 8080

CMD python main.py
