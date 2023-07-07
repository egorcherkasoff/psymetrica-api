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
