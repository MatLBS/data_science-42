import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
import sklearn.cluster as cluster
import matplotlib.ticker as mticker
import numpy as np

load_dotenv()


def elbow_method(cur):
    command_retrive_data = """
                SELECT user_id, COUNT(*) AS purchases
                FROM customers
                WHERE event_type = 'purchase'
                GROUP BY user_id
                ORDER BY purchases 25
            """

    cur.execute(command_retrive_data)
    data = cur.fetchall()
    data = np.array([x[1] for x in data]).reshape(-1, 1)
    
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "random_state": 1,
    }

    K=range(1, 11)
    wss = []
    for k in K:
        kmeans=cluster.KMeans(n_clusters=k, **kmeans_kwargs).fit(data)
        wss.append(kmeans.inertia_)

    sns.set(style="darkgrid")
    fig, ax = plt.subplots()

    ax.plot(K, wss)
    ax.set_xlabel('Number of Clusters')
    ax.set_xlim(0, 11)
    ax.set_title("The Elbow Method")

    # Remove Scientific Notation
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=False))
    ax.ticklabel_format(style='plain', axis='y')
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

    elbow_method(cur)

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
