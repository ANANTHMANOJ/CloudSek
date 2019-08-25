FROM python:3.7.0-alpine3.8
COPY ./requirements.txt ./
COPY ./ /cloudsek/
RUN apk update
RUN pip install --no-cache-dir -U pip
RUN apk add --virtual .build-deps gcc musl-dev libffi-dev
RUN apk add libpq
RUN apk add postgresql-dev
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /cloudsek/
CMD ["python3 flask_app.py"]