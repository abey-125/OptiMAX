# Importing Libraries
import pyodbc
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import date, datetime


def connection():
    # SQL Database Connection
    cnxn_str = ("Driver={SQL Server Native Client 11.0};"
                "Server=LAPTOP-T8RJOBVC\CFSQL;"
                "Database=Optimax;"
                "Trusted_Connection=yes;")
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()

    return cnxn


def most_selling_drug_preprocessing(cnxn):
    # Medicine table
    medicines = pd.read_sql_query (''' select * from medicines''', cnxn)
    medicines = pd.DataFrame(medicines)

    # orders table
    orders = pd.read_sql_query (''' select * from orders''', cnxn)
    orders = pd.DataFrame(orders)

    # order details table
    order_details = pd.read_sql_query (''' select * from order_details''', cnxn)
    order_details = pd.DataFrame(order_details)

    # Medicine vendor table
    medicine_vendor = pd.read_sql_query (''' select * from med_store''', cnxn)
    medicine_vendor = pd.DataFrame(medicine_vendor)

    # Store table
    store = pd.read_sql_query (''' select * from stores''', cnxn)
    store = pd.DataFrame(store)

    # Joining tables
    # Join medicine table and medicine vendor table
    medicine_store = medicines.merge(medicine_vendor, on = ['medicine_id','role_id'], how = 'inner')

    # Join medicine_store with store to get store name
    medicine_store = medicine_store.merge(store, on = ['store_id', 'role_id'], how = 'inner')

    # Join order and order details
    order_info = orders.merge(order_details, on = ['order_id', 'role_id'], how = 'inner')

    # Join orders and medicine store details
    medicine_order = order_info.merge(medicine_store, on = ['store_id', 'medicine_id', 'role_id'])


    return medicine_order


def filter_vendor_name(vendor, df, cnxn):

    # vendor table
    vendors = pd.read_sql_query (''' select * from vendors''', cnxn)
    vendors = pd.DataFrame(vendors)

    most_selling_drug_vendor = df.merge(vendors, on = ['vendor_id'], how = 'inner')
    # Filter to vendor name
    most_selling_drug_vendor = most_selling_drug_vendor[(most_selling_drug_vendor.vendor_name == vendor)] 

    return most_selling_drug_vendor

# Requirement 1

def most_selling_drug(most_selling_drug_vendor):

    # Viewing the most selling drug
    med_count = most_selling_drug_vendor.groupby(['medicine_name', 'store_id', 'store_name', 'vendor_id', 'vendor_name']).agg({'quantity' : 'sum'}).rename(columns={'quanity':'medicine_count'}).reset_index()
    # For each store the max selling drug
    med_count_max_by_Store = med_count.groupby(['store_id', 'vendor_id', 'store_name','vendor_name'])['quantity'].max().reset_index()

    med_count_max_by_Store = med_count_max_by_Store.merge(med_count, on  = ['store_id', 'vendor_id', 'store_name', 'quantity', 'vendor_name'], how='inner')

    # Display it as a bar plot
    # x axis has store name and y axis the medicine count
    fig = px.bar(med_count_max_by_Store, x="store_name", y="quantity", text="medicine_name",
    labels={"quantity": "MEDICINE COUNT","store_name": "STORE NAME "}, title="Most Selling Drug", 
    color_discrete_sequence =["#93D500"])

    #fig.update_xaxes(type='category')
    fig.show()
    return med_count_max_by_Store  

# Requirement 2

def most_selling_drug_by_time_frame(most_selling_drug_vendor):

    # Enter the time range
    enter_the_date_range_1= input('Enter a 1stdate: ')
    enter_the_date_range_2= input('Enter a 2nddate: ')

    # filtering by time range
    most_selling_drug_by_time = most_selling_drug_vendor[(most_selling_drug_vendor['date_created'] >= enter_the_date_range_1) & (most_selling_drug_vendor['date_created'] <= enter_the_date_range_2)]
    most_selling_drug_by_time.drop(['role_id_x', 'role_id_y'], axis = 1)

    # Viewing the most selling drug
    med_count = most_selling_drug_by_time.groupby(['medicine_name', 'store_id', 'store_name', 'vendor_id', 'vendor_name','date_created']).agg({'quantity' : 'sum'}).rename(columns={'quanity':'medicine_count'}).reset_index()
    # For each store the max selling drug
    med_count_max_by_Store = med_count.groupby(['store_id', 'vendor_id', 'store_name','vendor_name'])['quantity'].max().reset_index()

    med_count_max_by_Store = med_count_max_by_Store.merge(med_count, on  = ['store_id', 'vendor_id', 'store_name', 'quantity', 'vendor_name'], how='inner')

    # Display it as a bar plot
    # x axis has store name and y axis the medicine count
    fig = px.bar(med_count_max_by_Store, x="store_name", y="quantity", text="medicine_name",
    labels={"quantity": "MEDICINE COUNT","store_name": "STORE NAME "}, title="Most Selling Drug from" + " " + enter_the_date_range_1 + " " + "to" + " " + enter_the_date_range_2, 
    color_discrete_sequence =["#93D500"])

    # fig.update_xaxes(type='category')
    fig.show()
    return med_count_max_by_Store 
