import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_table(file_data, filename) -> None:
    columns = file_data.columns

    command_create = f"""
                CREATE TABLE IF NOT EXISTS {filename} (
                    {columns[0]} DATE,
                    {columns[1]} TEXT,
                    {columns[2]} INTEGER,
                    {columns[3]} REAL,
                    {columns[4]} BIGINT,
                    {columns[5]} VARCHAR(255)
                )
            """

    conn = psycopg2.connect(
          user=os.getenv('POSTGRES_LOGIN'),
          password=os.getenv('POSTGRES_PASSWORD'),
          host="localhost",
          port="5432",
          database=os.getenv('POSTGRES_NAME')
    )

    cur = conn.cursor()

    cur.execute(command_create)
    conn.commit()
    print("Table créée avec succès dans PostgreSQL")

    command_copy = f"""
                COPY {filename} ({columns[0]}, {columns[1]},
                {columns[2]}, {columns[3]}, {columns[4]}, {columns[5]})
                FROM '/tmp/{filename}.csv' DELIMITER ',' CSV HEADER;
            """
    cur.execute(command_copy)
    conn.commit()
    print("Table rempli avec succès dans PostgreSQL")

    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")


def read_file(path: str) -> None:
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"

    file_data = pd.read_csv(path)
    filename = path.split(".csv")[0].split('/')[1]
    create_table(file_data, filename)


def create_tables():
    path = (
        "/home/matle-br/Desktop/data_science-42/data_science_0/ex03/customer"
    )
    assert os.path.exists(path), "The folder does not exists"
    files = os.listdir(path)

    path = path.split('/')
    for file in files:
        read_file(path[len(path) - 1] + "/" + file)


def main():
    try:
        create_tables()
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
