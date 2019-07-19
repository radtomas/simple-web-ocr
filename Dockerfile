FROM python:3.7.4-alpine3.10

RUN apk add --upgrade --no-cache \
	musl-dev \
	gcc \
	zlib-dev \
	jpeg-dev \
	tesseract-ocr

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
