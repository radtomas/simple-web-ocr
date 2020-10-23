FROM python:3.7.4-alpine3.10

RUN apk add --upgrade --no-cache \
	musl-dev \
	gcc \
	zlib-dev \
	jpeg-dev \
	tesseract-ocr

RUN mkdir /code
COPY . /code/
WORKDIR /code
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
