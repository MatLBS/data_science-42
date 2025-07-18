import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_table(file_data, filename) -> None:
    columns = file_data.columns

    command = f"""
                CREATE TABLE IF NOT EXISTS {filename} (
                    {columns[0]} INTEGER,
                    {columns[1]} BIGINT,
                    {columns[2]} VARCHAR(255),
                    {columns[3]} TEXT
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

    command_copy = f"""
                COPY {filename} ({columns[0]}, {columns[1]},
                {columns[2]}, {columns[3]})
                FROM '/tmp/{filename}.csv' DELIMITER ',' CSV HEADER;
            """
    cur.execute(command_copy)
    conn.commit()
    print("Table rempli avec succès dans PostgreSQL")

    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")


def read_file(path: str, filename: str) -> None:
    assert isinstance(path, str), "The path must be a string"
    assert os.path.exists(path), "The file does not exists"
    assert path.endswith(".csv"), "The file extension must be csv"

    file_data = pd.read_csv(path)
    filename = filename.split(".csv")[0]
    create_table(file_data, filename)


def main():
    try:
        read_file("/home/matle-br/sgoinfre/subject/item/item.csv", "items.csv")
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
