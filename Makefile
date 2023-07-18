run dev:
	python manage.py runserver

migrations:
	python manage.py makemigrations && python manage.py migrate

format:
	isort . --skip env --skip migrations && black --exclude=migrations --exclude=env .

build:
	docker-compose build && docker-compose up --remove-orphans

down:
	docker-compose down

up:
	docker-compose up

createsuperuser:
	docker exec -it psymetrica-app python /app/manage.py createsuperuser