import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import seaborn as sns

load_dotenv()

def draw_chart1(cur):
    command_retrive_data = f"""
                SELECT DATE(event_time) AS day,
                    COUNT(DISTINCT user_id) AS unique_users
                FROM customers
                WHERE event_type = 'purchase'
                GROUP BY day
                ORDER BY day ASC;
            """

    cur.execute(command_retrive_data)
    results = cur.fetchall()

    y = []
    x = []
    for result in results:
        y.append(result[1])
        x.append(result[0])

    sns.set(style="darkgrid")
    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=1)
    locator = mdates.MonthLocator()
    fmt = mdates.DateFormatter('%b')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)
    
    ax.tick_params(axis='both', labelsize=7)
    ax.set_ylabel('Number of customers', fontsize = 7)

    plt.show()


def draw_chart2(cur):

    command_retrive_data = f"""
                SELECT 
                    EXTRACT(YEAR FROM event_time) AS year,
                    EXTRACT(MONTH FROM event_time) AS month,
                    SUM(price) AS total_value
                FROM customers
                WHERE event_type = 'purchase'
                GROUP BY year, month
                ORDER BY year, month;
            """
    
    cur.execute(command_retrive_data)
    results = cur.fetchall()
    
    y = []
    x = []
    for result in results:
        x.append(str(result[0]) + "-" + str(result[1]))
        y.append(result[2])
        
    print(y)

    sns.set(style="darkgrid")
    fig, ax = plt.subplots()
    ax.bar(pd.to_datetime(x, format="%Y-%m"), y, width=20)
    locator = mdates.MonthLocator()
    fmt = mdates.DateFormatter('%b')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)
    
    # plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

    ax.tick_params(axis='both', labelsize=7)
    ax.set_ylabel('Total sales in million of ₳', fontsize = 7)
    # ax.set_ylim(0, 1500000)
    ax.set_xlabel('month', fontsize = 7)

    plt.show()


def draw_chart3(cur):

    command_retrive_data = f"""
                SELECT DATE(event_time) AS day,
                    SUM(price) / COUNT(DISTINCT user_id)
                    AS average_spend
                FROM customers
                WHERE event_type = 'purchase'
                GROUP BY day
                ORDER BY day ASC;
            """

    cur.execute(command_retrive_data)
    results = cur.fetchall()

    y = []
    x = []
    for result in results:
        y.append(result[1])
        x.append(result[0])

    sns.set(style="darkgrid")
    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=1)
    locator = mdates.MonthLocator()
    fmt = mdates.DateFormatter('%b')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)
    
    ax.tick_params(axis='both', labelsize=7)
    ax.set_ylabel('Number of customers', fontsize = 7)

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
        
        # draw_chart1(cur)
        draw_chart2(cur)
        # draw_chart3(cur)

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