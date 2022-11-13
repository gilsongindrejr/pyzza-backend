#!/bin/bash

docker-compose down;
docker volume rm docker_app_data;
docker-compose up --build;
