import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def merge_tables():
    command_merge = f"""
                CREATE TEMPORARY TABLE temp_customers AS (
					SELECT CASE when i.product_id is null then c.product_id else i.product_id end as product_id
						, event_time, event_type, price, user_id, user_session
						, category_id, category_code, brand
					FROM customers c
					FULL JOIN item i
					ON c.product_id = i.product_id
                );
				TRUNCATE customers;
				ALTER TABLE customers
				ADD COLUMN category_id BIGINT,
				ADD COLUMN category_code VARCHAR(255),
				ADD COLUMN brand TEXT;
                INSERT INTO customers 
				SELECT * FROM temp_customers;
            """

    conn = psycopg2.connect(
          user=os.getenv('POSTGRES_LOGIN'),
          password=os.getenv('POSTGRES_PASSWORD'),
          host="localhost",
          port="5432",
          database=os.getenv('POSTGRES_NAME')
    )

    cur = conn.cursor()

    cur.execute(command_merge)
    conn.commit()
    print("Tables fusionnées avec succès dans PostgreSQL")

    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")


def create_table(file_data, filename) -> None:
    columns = file_data.columns

    command_create = f"""
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

    cur.execute(command_create)
    conn.commit()
    print("Table créée avec succès dans PostgreSQL")

    command_copy = f"""
                COPY {filename} ({columns[0]}, {columns[1]}, {columns[2]}, {columns[3]})
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
    filename = "item"
    create_table(file_data, filename)

def main():
    try:
        read_file("/Users/mateolebrassancho/Documents/42/data_science-42/"
        "data_science_1/ex00/item/item.csv")
        merge_tables()
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
