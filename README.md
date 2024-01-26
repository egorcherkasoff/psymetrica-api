# Psymetrica API


**Psymetrica** - это платформа для тестов по психологии, на которой психологи могут создавать и назначать пользователям тесты, а они их проходить.

_Учтите, что проект еще в процессе разработки, могут присутствовать баги, нереализованный функционал!_

Для запуска dev-версии вам необходимо создать .env файл в корневой папке проекта со следующим содержимым:

```
SECRET_KEY=your secret key
DEBUG=True or False
POSTGRES_USER=database user
POSTGRES_PASSWORD=database password
POSTGRES_DB=database name
POSTGRES_HOST=database host
POSTGRES_PORT=database port
CELERY_BROKER=redis url
CELERY_BACKEND=redis url
DOMAIN=domain
EMAIL_PORT=email port
CELERY_FLOWER_USER=flower admin user
CELERY_FLOWER_PASSWORD=flower admin password
```

Пример:

```
SECRET_KEY=mysecret_key
DEBUG=True
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
POSTGRES_DB=psymetrica
POSTGRES_HOST=db
POSTGRES_PORT=5432
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0
DOMAIN=localhost:8000
EMAIL_PORT=1025
CELERY_FLOWER_USER=admin
CELERY_FLOWER_PASSWORD=123123
```

Если вы используете пример .env файла указанный мной, далее вам необходимо прописать следующие команды в терминале (если у вас установлен docker, docker-compose):

```
docker-compose build
```

```
docker-compose up
```

После завершения сборки и запуска, откройте браузер и перейдите по адресу http://localhost:8080/redoc, чтобы открыть документацю API в формате **Redocly** (openapi)

Также вы можете создать супер пользователя с помощью команды ниже:

```
docker exec -it psymetrica-app python /app/manage.py createsuperuser
```

Для создания example data, вы можете воспользоваться этой командой:

```
docker exec -it psymetrica-app python /app/manage.py prepopulate
```

Чтобы зайти в панель администратора, перейдите на http://localhost:8080/admin, после чего введите данные для входа.

