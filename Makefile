build:
	docker-compose -f build/Dockefile build

run:
	docker-compose -f build/docker-compose.yaml up -d

stop_db:
	docker-compose -f build/docker-compose.yaml stop db

start_db:
	docker-compose -f build/docker-compose.yaml start db

restart_api:
	docker-compose -f build/docker-compose.yaml stop api
	docker-compose -f build/docker-compose.yaml up -d api

stop_api:
	docker-compose -f build/docker-compose.yaml stop server
