# Uklon Test Case


## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)


## Swagger
- [localhost:8000/docs](http://localhost:8000/docs)

## Run

```sh
$ git clone git@github.com:Twenty1th/Uklon-test-task.git
$ cd Uklon-test-task
$ make build-image
$ make run
```

## Test the api when the database is disabled
```sh
$ make stop-db
$ make api-logs
$ make start-db
```

## Makefile Targets

Build the Docker images defined in the Dockerfile.

```sh
$ make build
```
Start the services defined in docker-compose.yaml in detached mode.

```sh
$ make run
```
Stop the database service.

```sh
$ make stop-db
```
Start the database service.
```sh
$ make start-db.
```
Restart the API service.
```sh
$ make restart-api
```
Stop the API service.
```sh
$ make stop-api
```
API logs
```sh
$ make api-logs
```
Randomizer logs
```sh
$ make api-logs
```

