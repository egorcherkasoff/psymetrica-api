FROM python:3.11.1-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get install -y build-essential libpq-dev

WORKDIR /app

COPY ./requirements .

COPY . .

RUN pip install --upgrade pip

RUN pip install -r local.txt

# django run
COPY ./docker/django/start.sh /start

RUN sed -i 's/\r$//' /start

RUN chmod +x /start

# celery
COPY ./docker/celery/start.sh /start-celery

RUN sed -i 's/\r$//' /start-celery

RUN chmod +x /start-celery

# flower

COPY ./docker/flower/start.sh /start-flower

RUN sed -i 's/\r$//' /start-flower

RUN chmod +x /start-flower



# CMD ["/bin/bash", "./docker/django/start.sh"]
