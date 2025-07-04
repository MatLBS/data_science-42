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
from datetime import datetime

load_dotenv()


def clustering(cur):

    command_retrive_data = """
                SELECT DISTINCT user_id,
                    MIN(event_time) OVER (PARTITION BY user_id) AS first_purchase_date,
                    MAX(event_time) OVER (PARTITION BY user_id) AS last_purchase_date,
                    CASE
                            WHEN MAX(event_time) OVER (PARTITION BY user_id) < '2022-12-30' THEN 'inactive'
                            WHEN MIN(event_time) OVER (PARTITION BY user_id) < '2023-02-15' 
                                AND COUNT(event_time) OVER (PARTITION BY user_id) > 20 THEN 'platinium'
                            WHEN MIN(event_time) OVER (PARTITION BY user_id) < '2023-02-15' 
                                AND COUNT(event_time) OVER (PARTITION BY user_id) > 10 THEN 'gold'
                            ELSE 'new'
                    END AS client_type,
                    COUNT(event_time) OVER (PARTITION BY user_id) AS number_purchase
                FROM customers
                WHERE event_type = 'purchase'
            """

    cur.execute(command_retrive_data)
    data = cur.fetchall()

    # data_customers = [x[3] for x in data]
    # gold = data_customers.count("gold")
    # platinium = data_customers.count("platinium")
    # inactive = data_customers.count("inactive")
    # new = data_customers.count("new")

    # x = [gold, platinium, new, inactive]
    # y = ["gold", "platinium", "new", "inactive"]
    # colors = ["#FFD700", "#E5E4E2", "#87CEEB", "#A9A9A9"]

    # fig, ax = plt.subplots()
    # ax.barh(y, x, color=colors, align='center')
    # ax.invert_yaxis()

    # def add_labels(x, y):
    #     for i in range(len(x)):
    #         plt.text(x[i] + 500, i, str(x[i]))

    # add_labels(x, y)
    # ax.tick_params(axis='both', labelsize=7)
    # ax.set_xlabel('Number of customers', fontsize=7)

    def months_diff(date1_str, date2_str):
        date1 = datetime.strptime(date1_str, "%Y-%m-%d")
        date2 = datetime.strptime(date2_str, "%Y-%m-%d")

        diff_years = date2.year - date1.year
        diff_months = date2.month - date1.month

        return diff_years * 12 + diff_months

    gold_median_freq = np.median([x[4] for x in data if x[3] == 'gold'])
    gold_median_rec = np.median([months_diff(str(x[2]), "2023-02-28") for x in data if x[3] == 'gold'])
    platinium_median_freq = np.median([x[4] for x in data if x[3] == 'platinium'])
    platinium_median_rec = np.median([months_diff(str(x[2]), "2023-02-28") for x in data if x[3] == 'platinium'])
    inactive_median_freq = np.median([x[4] for x in data if x[3] == 'inactive'])
    inactive_median_rec = np.median([months_diff(str(x[2]), "2023-02-28") for x in data if x[3] == 'inactive'])
    new_median_freq = np.median([x[4] for x in data if x[3] == 'new'])
    new_median_rec = np.median([months_diff(str(x[2]), "2023-02-28") for x in data if x[3] == 'new'])

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
