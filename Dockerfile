FROM python:3.11.1-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get install -y build-essential libpq-dev

WORKDIR /app

COPY ./requirements .

COPY . .

RUN pip install --upgrade pip

RUN pip install -r local.txt

RUN chmod +x start.sh

ENTRYPOINT [ "start.sh" ]