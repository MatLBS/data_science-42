import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def remove_duplicates() -> None:

    command_remove = f"""
                CREATE TEMPORARY TABLE temp_customers AS 
                SELECT DISTINCT * FROM customers;
                TRUNCATE customers;
                INSERT INTO customers SELECT * FROM temp_customers;
            """

    conn = psycopg2.connect(
          user=os.getenv('POSTGRES_LOGIN'),
          password=os.getenv('POSTGRES_PASSWORD'),
          host="localhost",
          port="5432",
          database=os.getenv('POSTGRES_NAME')
    )

    cur = conn.cursor()

    cur.execute(command_remove)
    conn.commit()
    print("Doublons supprimés avec succès dans PostgreSQL")

    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")


def main():
    try:
        remove_duplicates()
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
