import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_table(file_data, filename) -> None:
    columns = file_data.columns

    command = f"""
                CREATE TABLE {filename} (
                    event_id SERIAL PRIMARY KEY,
                    {columns[0]} DATE NOT NULL,
                    {columns[1]} TEXT NOT NULL,
                    {columns[2]} INTEGER NOT NULL,
                    {columns[3]} REAL NOT NULL,
                    {columns[4]} BIGINT NOT NULL,
                    {columns[5]} VARCHAR(255) NOT NULL
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

    cur.execute(command)
    conn.commit()
    print("Table créée avec succès dans PostgreSQL")

    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")


def read_file(path: str) -> None:
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"

    file_data = pd.read_csv(path)
    filename = path.split(".csv")[0].split('/')[1]
    print(filename)
    create_table(file_data, filename)


def create_tables():
    path = (
        "/Users/mateolebrassancho/Documents/42/data_science-42/"
        "data_science_0/ex03/customer"
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
