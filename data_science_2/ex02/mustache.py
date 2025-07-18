import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns

load_dotenv()


def draw_first_charts(cur):
    command_retrive_data = """
                SELECT price
                FROM customers
                WHERE event_type = 'purchase'
            """

    cur.execute(command_retrive_data)
    results = cur.fetchall()
    results = [result[0] for result in results]

    df = pd.DataFrame(results)

    print(df.describe().apply(lambda s: s.apply('{0:.5f}'.format)))

    sns.set(style="darkgrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    box = ax1.boxplot(results, vert=False, widths=0.8, patch_artist=True)
    for patch in box['boxes']:
        patch.set_facecolor('lightgreen')
    for patch in box['medians']:
        patch.set_color('black')
    ax1.set_yticks([])
    ax1.tick_params(axis='both', labelsize=7)
    ax1.set_xlabel('price', fontsize=7)

    box = ax2.boxplot(
        results, vert=False, widths=0.8, patch_artist=True, showfliers=False
    )
    for patch in box['boxes']:
        patch.set_facecolor('lightgreen')
    for patch in box['medians']:
        patch.set_color('black')
    ax2.set_yticks([])
    ax2.tick_params(axis='both', labelsize=7)
    ax2.set_xlabel('price', fontsize=7)

    ax2.set_xlim(-1, 13)
    plt.show()


def draw_chart3(cur):
    command_retrive_data = """
                SELECT user_id, AVG(price) AS avg_cart_price
                FROM customers
                WHERE event_type = 'cart'
                GROUP BY user_id
                HAVING AVG(price) BETWEEN 26 AND 43;
            """

    cur.execute(command_retrive_data)
    results = cur.fetchall()
    results = [result[1] for result in results]

    sns.set(style="darkgrid")
    fig, ax = plt.subplots()

    box = ax.boxplot(
        results, vert=False, widths=0.8, patch_artist=True, showfliers=True
    )

    for patch in box['boxes']:
        patch.set_facecolor('lightblue')
    for patch in box['medians']:
        patch.set_color('black')

    ax.set_yticks([])
    ax.set_xticks(range(26, 43, 2))
    ax.tick_params(axis='both', labelsize=7)
    ax.set_xlabel('price', fontsize=7)

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

    draw_first_charts(cur)
    draw_chart3(cur)

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
