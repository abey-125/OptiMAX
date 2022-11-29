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

# Join medicine table and medicine vendor table
medicine_store = medicines_df.merge(medicine_vendor, on = ['medicine_id','role_id'], how = 'left')

# Join medicine_store with store to get store name
medicine_store = medicine_store.merge(store, on = ['store_id'], how = 'left')

# Viewing the most selling drug
med_count = medicine_store.groupby(['medicine_name', 'store_id', 'store_name']).agg({'medicine_name' : 'count'}).rename(columns={'medicine_name':'medicine_count'}).reset_index()

# For each store the max selling drug
med_count_max_by_Store = med_count.groupby(['medicine_name', 'store_id', 'store_name']).max().reset_index()
med_count_max_by_Store

# Display it as a bar plot
# x axis has store name and y axis the medicine count
fig = px.bar(med_count_max_by_Store, x="store_name", y="medicine_count", text="medicine_name", title="Most Selling Drug", 
color_discrete_sequence =["#93D500"])
fig.update_xaxes(type='category')
fig.show()

