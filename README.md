# Project Name

This project uses Docker Compose to manage the development and deployment environment. Below are the available Makefile targets to build and run the project.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Makefile Targets

### `build`

Build the Docker images defined in the Dockerfile.

```sh
make build
```
Start the services defined in docker-compose.yaml in detached mode.

```sh
make run
```
Stop the database service.

```sh
make stop_db
```
Start the database service.
```sh
make start_db.
```
Restart the API service.
```sh
make restart_api
```
Stop the API service.
```sh
make stop_api
```