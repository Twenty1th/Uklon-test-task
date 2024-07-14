build-image:
	docker build -f build/Dockerfile -t uklon-api-server .

run:
	docker-compose -f build/docker-compose.yaml up -d

stop:
	docker-compose -f build/docker-compose.yaml stop

api-logs:
	docker logs -f --tail 100 api-server

randomizer-logs:
	docker logs -f --tail 100 randomizer-server

stop-db:
	docker-compose -f build/docker-compose.yaml stop db

start-db:
	docker-compose -f build/docker-compose.yaml start db

restart-api:
	docker-compose -f build/docker-compose.yaml stop api
	docker-compose -f build/docker-compose.yaml up -d api

stop-api:
	docker-compose -f build/docker-compose.yaml stop server
