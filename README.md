# Psymetrica API

To run create .env file with following data:

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

For example

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

Then run

```
docker-compose build
```

```
docker-compose up
```

Now navigate to https://localhost:8080 and site should be working

You can also create superuser with following command

```
make createsuperuser
```

or

```
docker exec -it psymetrica-app python /app/manage.py createsuperuser
```
