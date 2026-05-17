run:
	flask --app backend.app run --debug

test:
	pytest backend/tests/ -v

migrate:
	flask --app backend.app db migrate -m "$(msg)"

upgrade:
	flask --app backend.app db upgrade

init-db:
	flask --app backend.app db init
	flask --app backend.app db migrate -m "initial"
	flask --app backend.app db upgrade

docker:
	docker-compose up --build

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

