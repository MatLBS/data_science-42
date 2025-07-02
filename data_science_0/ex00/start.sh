#!/bin/bash

docker rm -f /postgres
docker rm -f /pgadmin4_container

docker-compose up -d