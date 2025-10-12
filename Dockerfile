FROM python:3.12-alpine3.17

WORKDIR /app
COPY . ./

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -Ur requirements.txt \
    && apk del .build-deps

EXPOSE 8080

CMD ["python" ,"main.py"]
