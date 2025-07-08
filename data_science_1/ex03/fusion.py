import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def merge_tables():
    command_merge = """
                ALTER TABLE IF EXISTS customers
                ADD category_id bigint[],
                ADD category_code text[],
                ADD brand text[];
                CREATE TEMPORARY TABLE temp AS (
                    SELECT product_id,
                    ARRAY_AGG(DISTINCT category_id)
                    FILTER(WHERE category_id IS NOT NULL) AS category_id,
                    ARRAY_AGG(DISTINCT category_code)
                    FILTER(WHERE category_code IS NOT NULL) AS category_code,
                    ARRAY_AGG(DISTINCT brand)
                    FILTER(WHERE brand IS NOT NULL) AS brand
                    FROM items
                    GROUP BY product_id
                );
                UPDATE customers
                SET category_id=temp.category_id,
                category_code=temp.category_code, brand=temp.brand
                FROM temp
                WHERE customers.product_id=temp.product_id
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
