#!/bin/bash

docker rm -f /postgres
docker rm -f /pgadmin4_container

docker-compose up -d

docker cp ~/sgoinfre/subject/customer/data_2022_dec.csv postgres:/tmp/data_2022_dec.csv
docker cp ~/sgoinfre/subject/customer/data_2022_nov.csv postgres:/tmp/data_2022_nov.csv
docker cp ~/sgoinfre/subject/customer/data_2022_oct.csv postgres:/tmp/data_2022_oct.csv
docker cp ~/sgoinfre/subject/customer/data_2023_jan.csv postgres:/tmp/data_2023_jan.csv
docker cp ~/sgoinfre/subject/customer/data_2023_feb.csv postgres:/tmp/data_2023_feb.csv

docker cp ~/sgoinfre/subject/item/item.csv postgres:/tmp/items.csv

python3 automatic_table.py
python3 items_table.py