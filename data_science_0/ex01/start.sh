#!/bin/bash

docker rm -f /postgres
docker rm -f /pgadmin4_container

docker-compose up -d

docker cp /home/matle-br/sgoinfre/subject/customer/data_2022_dec.csv postgres:/tmp/data_2022_dec.csv
docker cp /home/matle-br/sgoinfre/subject/customer/data_2022_nov.csv postgres:/tmp/data_2022_nov.csv
docker cp /home/matle-br/sgoinfre/subject/customer/data_2022_oct.csv postgres:/tmp/data_2022_oct.csv
docker cp /home/matle-br/sgoinfre/subject/customer/data_2023_jan.csv postgres:/tmp/data_2023_jan.csv
docker cp /home/matle-br/sgoinfre/subject/item/item.csv postgres:/tmp/items.csv