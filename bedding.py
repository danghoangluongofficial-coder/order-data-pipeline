from fastapi import FastAPI, HTTPException #import FastAPI like an object
from typing import Optional, Dict
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector


app = FastAPI()

load_dotenv()
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password = os.environ.get("THE_SECRET_SAUCE"),
        database="mattress_api"
    )


# mysql.connector.connect call the connect method. Once connect, 
# will handle "active link"
# host="localhost" # Tells Python where data base is located, localhost mean 
# database server run on same computer as your Python script
# username used to log in to MySQL. root is the default administrative user with full permissions.
# password = password u set on SQL
# database tells python whuch folder schema inside MySQL to open

@app.get("/")
def index():
    return {"message": "API is running"}

@app.get("/products")
def get_products():
    conn = get_db() # Connect python to SQL
    cursor = conn.cursor(dictionary=True) #browsing through data in dictionary form

    cursor.execute("SELECT * FROM products WHERE sku LIKE 'BLC%'") #choose methods to run on SQL
    # Put SQL code in this function
    products = cursor.fetchall() #retrieves all the rows that the SQL query found 
    # in products and turn them into a Python List 

    cursor.close()
    conn.close()

    return products

class OrderRequest(BaseModel):
    customer: str
    items: Dict[str,int]

@app.post("/create-orders")
# Get the products we are looking for from the orders
def create_order(order: OrderRequest):
    conn = get_db() # Connect
    cursor = conn.cursor(dictionary=True)
    for sku, qty in order.items.items():
        cursor.execute("SELECT * FROM products WHERE sku = %s",(sku,))
        product = cursor.fetchone() # selected row in products
        # conn.cursor creaete a pointer that travels into the database
        # dictionary=True tells the cursor to return each database row
        # as a Python dictionary

    # Check if the products exist:
        if product is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail='Product not found')
        
    #Check if order quantity is valid:
        if qty <= 0:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail='Order quantity must be at least 1')
        
    #Check if enough stock exist:
        if product['stock'] <= qty:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail='Not enough product!')

    #Put on orders list
    #--------------------------------------------------------
    # If it goes through here there are available products
        unit_price = product['price']
        revenue = qty*unit_price

    # Insert orders in order tables
        cursor.execute(
            """
            INSERT INTO orders(
                customer_name,
                sku,
                quantity,
                unit_price,
                order_revenue
            )
            VALUES (%s,%s,%s,%s,%s)
            """,
            (order.customer,sku,qty,unit_price,revenue)
        )
         # New Order ID
        new_order_id = cursor.lastrowid
        conn.commit()#This saves: INSERT (order) and UPDATE (stock)

        # Update stocks and so on
        cursor.execute(
            """
            UPDATE products
            SET stock = stock - %s
            WHERE sku = %s
            """,
            (qty, sku)
        )
        # Save all changes
        conn.commit()


    cursor.close()
    conn.close()

    # Return message
    return {
        "message": "Order created successfully",
        "order_id": new_order_id,
        "customer": order.customer,
        "ordered items": order.items,
        "unit_price": unit_price,
        "revenue": revenue,
    }