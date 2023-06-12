MANAGE := poetry run python3 manage.py

install:
	poetry install

start:
	${MANAGE} runserver

lint:
	poetry run flake8 .

test:
	${MANAGE} test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml --omit=*/tests/*,*tests.py,*/migrations/*,*__init__.py,*settings.py,*manage.py
	poetry run coverage report --omit=*/tests/*,*tests.py,*/migrations/*,*__init__.py,*settings.py,*manage.py

shell:
	${MANAGE} shell

requirements:
	poetry export -f requirements.txt --without-hashes -o requirements.txt