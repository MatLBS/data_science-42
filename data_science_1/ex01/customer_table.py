import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def merge_tables() -> None:

    command_merge = """
                CREATE TABLE IF NOT EXISTS customers AS
                (
                    SELECT * FROM data_2022_dec
                    UNION ALL
                    SELECT * FROM data_2022_nov
                    UNION ALL
                    SELECT * FROM data_2022_oct
                    UNION ALL
                    SELECT * FROM data_2023_feb
                    UNION ALL
                    SELECT * FROM data_2023_jan
                );
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


def main():
    try:
        merge_tables()
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
