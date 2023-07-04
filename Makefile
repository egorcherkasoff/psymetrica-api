run dev:
	python manage.py runserver

migrations:
	python manage.py makemigrations && python manage.py migrate

format:
	isort . --skip env --skip migrations && black --exclude=migrations --exclude=env .