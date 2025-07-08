import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def remove_duplicates() -> None:

    command_remove = """
                CREATE TABLE IF NOT EXISTS new_customers AS
                (
                    SELECT event_type, product_id,
                    user_id, user_session, count(*)
                    FROM customers
                    GROUP BY event_type, product_id, user_id, user_session
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

    cur.execute(command_remove)
    conn.commit()
    print("Table créée avec succès dans PostgreSQL")

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
