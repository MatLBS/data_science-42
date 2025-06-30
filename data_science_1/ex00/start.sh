#!/bin/bash

docker-compose up -d

docker cp /Users/mateolebrassancho/Documents/42/data_science-42/data_science_1/ex00/customer/data_2022_dec.csv postgres:/tmp/data_2022_dec.csv
docker cp /Users/mateolebrassancho/Documents/42/data_science-42/data_science_1/ex00/customer/data_2022_nov.csv postgres:/tmp/data_2022_nov.csv
docker cp /Users/mateolebrassancho/Documents/42/data_science-42/data_science_1/ex00/customer/data_2022_oct.csv postgres:/tmp/data_2022_oct.csv
docker cp /Users/mateolebrassancho/Documents/42/data_science-42/data_science_1/ex00/customer/data_2023_jan.csv postgres:/tmp/data_2023_jan.csv
docker cp /Users/mateolebrassancho/Documents/42/data_science-42/data_science_1/ex00/customer/data_2023_feb.csv postgres:/tmp/data_2023_feb.csv

docker cp /Users/mateolebrassancho/Documents/42/data_science-42/data_science_1/data/item/item.csv postgres:/tmp/item.csv

python3 automatic_table.py