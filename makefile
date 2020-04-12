make:
	vim makefile

venv:
	virtualenv -p python3 venv

deps:
	# https://docs.docker.com/compose/install/
	./venv/bin/pip3 install -r requirements.txt

run:
	./venv/bin/uvicorn main:app --reload

up:
	docker-compose up -d

psql:
	docker-compose exec db psql -U s3http
