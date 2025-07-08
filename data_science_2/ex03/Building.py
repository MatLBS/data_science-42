import os
import psycopg2
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns

load_dotenv()


def draw_charts(cur):
    command_retrive_orders = """
                SELECT COUNT(user_id)
                FROM customers
                WHERE event_type = 'purchase'
                GROUP BY user_id
            """

    command_retrive_spending = """
                SELECT SUM(price) AS count, user_id
                FROM customers
                WHERE event_type = 'purchase'
                GROUP BY user_id
                HAVING SUM(price) < 225
            """

    cur.execute(command_retrive_orders)
    data_orders = cur.fetchall()
    data_orders = [result[0] for result in data_orders if result[0] <= 40]

    cur.execute(command_retrive_spending)
    data_spending = cur.fetchall()
    data_spending = [result[0] for result in data_spending]

    sns.set(style="darkgrid")
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    ax[0].hist(data_orders, bins=5)

    ax[0].tick_params(axis='both', labelsize=7)
    ax[0].set_ylabel('customers', fontsize=7)
    ax[0].set_xlabel('frequency', fontsize=7)
    ax[0].set_xticks(range(0, 45, 10))

    ax[1].hist(data_spending, bins=5)

    ax[1].tick_params(axis='both', labelsize=7)
    ax[1].set_ylabel('customers', fontsize=7)
    ax[1].set_xlabel('monetary value in ₳', fontsize=7)

    plt.show()


def call_data():
    conn = psycopg2.connect(
        user=os.getenv('POSTGRES_LOGIN'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host="localhost",
        port="5432",
        database=os.getenv('POSTGRES_NAME')
    )
    cur = conn.cursor()

    draw_charts(cur)

    conn.commit()
    cur.close()
    conn.close()


def main():
    try:
        call_data()
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()
