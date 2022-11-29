# Importing Libraries
import pyodbc
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# SQL Database Connection
cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=LAPTOP-T8RJOBVC\CFSQL;"
            "Database=Optimax;"
            "Trusted_Connection=yes;")
cnxn = pyodbc.connect(cnxn_str)
cursor = cnxn.cursor()

##### Requirement 1: view the most selling drug by store

# Medicine Table
medicines = pd.read_sql_query (''' select * from medicines''', cnxn)
medicines_df = pd.DataFrame(medicines)
medicines_df

# Medicine vendor table
medicine_vendor = pd.read_sql_query (''' select * from med_store''', cnxn)
medicine_vendor = pd.DataFrame(medicine_vendor)
medicine_vendor

# store table
store = pd.read_sql_query (''' select * from stores''', cnxn)
store = pd.DataFrame(store)

# orders Table
orders = pd.read_sql_query (''' select * from orders''', cnxn)
orders = pd.DataFrame(orders)
orders

# order details Table
order_details = pd.read_sql_query (''' select * from order_details''', cnxn)
order_details = pd.DataFrame(order_details)
order_details

# Join medicine table and medicine vendor table
medicine_store = medicines_df.merge(medicine_vendor, on = ['medicine_id','role_id'], how = 'inner')

# Join medicine_store with store to get store name
medicine_store = medicine_store.merge(store, on = ['store_id', 'role_id'], how = 'inner')

# Join order and order details
order_info = orders.merge(order_details, on = ['order_id', 'role_id'], how = 'inner')

# Join orders and medicine store details
medicine_order = order_info.merge(medicine_store, on = ['store_id', 'medicine_id', 'role_id'], how = 'inner')

# Viewing the most selling drug
med_count = medicine_order.groupby(['medicine_name', 'store_id', 'store_name']).agg({'quantity' : 'sum'}).rename(columns={'quanity':'medicine_count'}).reset_index()

# For each store the max selling drug
med_count_max_by_Store = med_count.groupby(['medicine_name', 'store_id']).max().reset_index()

# Display it as a bar plot
# x axis has store name and y axis the medicine count
fig = px.bar(med_count_max_by_Store, x="store_name", y="quantity", text="medicine_name", 
labels={"quantity": "MEDICINE COUNT","store_name": "STORE NAME "},title="Most Selling Drug", 
color_discrete_sequence =["#93D500"])
fig.update_xaxes(type='category')
fig.show()

##### Requirement 2: The system shall allow selecting the time window and display the store with most selling drug



