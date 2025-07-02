import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()

def draw_pie():
    command_retrive_data = f"""
                SELECT event_type FROM customers
            """
    
    conn = psycopg2.connect(
          user=os.getenv('POSTGRES_LOGIN'),
          password=os.getenv('POSTGRES_PASSWORD'),
          host="localhost",
          port="5432",
          database=os.getenv('POSTGRES_NAME')
    )
    
    cur = conn.cursor()
    cur.execute(command_retrive_data)
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    view = results.count(('view',))
    purchase = results.count(('purchase',))
    remove_from_cart = results.count(('remove_from_cart',))
    cart = results.count(('cart',))

    y = [view, cart, remove_from_cart, purchase]
    mylabels = ["view", "cart", "remove_from_cart", "purchase"]

    plt.pie(y, labels = mylabels, autopct="%1.1f%%")
    plt.show() 


def main():
    try:
        draw_pie()
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == "__main__":
    main()