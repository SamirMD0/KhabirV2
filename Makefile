# -- Backend -------------------------------------------------
run-api:
	flask --app backend.app run --debug --port 5000

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

# -- Frontend ------------------------------------------------
install-frontend:
	cd frontend && npm install

run-frontend:
	cd frontend && npm run dev

build-frontend:
	cd frontend && npm run build

# -- Combined ------------------------------------------------
dev:
	make run-api & make run-frontend

install:
	pip install -r requirements.txt && cd frontend && npm install

# -- Docker --------------------------------------------------
docker:
	docker-compose up --build
