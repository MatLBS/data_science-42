import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
import matplotlib.ticker as mticker
import numpy as np
from datetime import datetime
from sklearn.cluster import KMeans


load_dotenv()


def clustering(cur):

    command_retrive_data = """
                 SELECT DISTINCT user_id,
                    CASE
                            WHEN MAX(event_time) OVER (PARTITION BY user_id) < '2022-12-30' THEN 'inactive'
                            WHEN MIN(event_time) OVER (PARTITION BY user_id) < '2023-02-15' 
                                AND COUNT(event_time) OVER (PARTITION BY user_id) > 20 THEN 'platinium'
                            WHEN MIN(event_time) OVER (PARTITION BY user_id) < '2023-02-15' 
                                AND COUNT(event_time) OVER (PARTITION BY user_id) > 10 THEN 'gold'
                            ELSE 'new'
                    END AS client_type,
                    COUNT(event_time) OVER (PARTITION BY user_id) AS number_purchase,
                    SUM(price) OVER (PARTITION BY user_id) AS sum_purchase
                FROM customers
                WHERE event_type = 'purchase'
            """

    cur.execute(command_retrive_data)
    data = cur.fetchall()
    data = np.array([[x[2], x[3]] for x in data])
    nb_clusters = 4
    
    colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'orange', 'purple', 'brown', 'pink']
    
    kmeans = KMeans(n_clusters=nb_clusters, random_state=1, n_init=10).fit(data)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    
    # plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis', label='Data points')
    for i in range(nb_clusters):
        plt.scatter(
            data[labels == i, 0], 
            data[labels == i, 1], 
            c=colors[i], 
            label=f'Cluster {i+1}', 
            s=30
        )
    plt.scatter(centroids[:,0] , centroids[:,1] , s = 80, color = 'red', label='Centroids', edgecolor='black')
    plt.title('Clusters')
    plt.xlabel('Number of Purchases')
    plt.ylabel('Total Purchase Amount')
    plt.legend()





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

    clustering(cur)

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
    
