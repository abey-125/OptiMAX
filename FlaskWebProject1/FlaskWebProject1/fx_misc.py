# Importing Libraries
import pyodbc
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import date, datetime

# Author : Chinnu Treesa Fulton

def connection():
    # SQL Database Connection
    cnxn_str = ("Driver={SQL Server Native Client 11.0};"
                # Change the server name 
                "Server=LAPTOP-T8RJOBVC\CFSQL;"
                "Database=Optimax;"
                "Trusted_Connection=yes;")
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()

    return cnxn

############################# SALE ANALYTICS SUPPLIER ####################################################

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

    most_selling_drug_vendor = df.merge(vendors, on = ['vendor_id', 'vendor_name'], how = 'inner')
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
    med_count_max_by_Store = med_count_max_by_Store.drop(['store_id','vendor_id','vendor_name'], axis = 1)
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
    med_count_max_by_Store = med_count_max_by_Store.drop(['store_id','vendor_id','vendor_name'], axis = 1)
    # Display it as a bar plot
    # x axis has store name and y axis the medicine count
    fig = px.bar(med_count_max_by_Store, x="store_name", y="quantity", text="medicine_name",
    labels={"quantity": "MEDICINE COUNT","store_name": "STORE NAME "}, title="Most Selling Drug from" + " " + enter_the_date_range_1 + " " + "to" + " " + enter_the_date_range_2, 
    color_discrete_sequence =["#93D500"])

    # fig.update_xaxes(type='category')
    fig.show()
    return med_count_max_by_Store 

# Requirement 3
def least_selling_drug_by_time_frame(least_selling_drug_vendor):

    # Enter the time range
    enter_the_date_range_1= input('Enter a 1stdate: ')
    enter_the_date_range_2= input('Enter a 2nddate: ')

    # filtering by time range
    least_selling_drug_by_time = least_selling_drug_vendor[(least_selling_drug_vendor['date_created'] >= enter_the_date_range_1) & (least_selling_drug_vendor['date_created'] <= enter_the_date_range_2)]
    least_selling_drug_by_time.drop(['role_id_x', 'role_id_y'], axis = 1)

    # Viewing the most selling drug
    med_count = least_selling_drug_by_time.groupby(['medicine_name', 'store_id', 'store_name', 'vendor_id', 'vendor_name','date_created']).agg({'quantity' : 'sum'}).rename(columns={'quanity':'medicine_count'}).reset_index()
    # For each store the max selling drug
    med_count_min_by_Store = med_count.groupby(['store_id', 'vendor_id', 'store_name','vendor_name'])['quantity'].min().reset_index()

    med_count_min_by_Store = med_count_min_by_Store.merge(med_count, on  = ['store_id', 'vendor_id', 'store_name', 'quantity', 'vendor_name'], how='inner')
    med_count_min_by_Store = med_count_min_by_Store.drop(['store_id','vendor_id','vendor_name'], axis = 1)
    # Display it as a bar plot
    # x axis has store name and y axis the medicine count
    fig = px.bar(med_count_min_by_Store, x="store_name", y="quantity", text="medicine_name",
    labels={"quantity": "MEDICINE COUNT","store_name": "STORE NAME "}, title="Least Selling Drug from" + " " + enter_the_date_range_1 + " " + "to" + " " + enter_the_date_range_2, 
    color_discrete_sequence =["#93D500"])

    # fig.update_xaxes(type='category')
    fig.show()
    return med_count_min_by_Store

# Requirement 3

def view_store_by_location(cnxn):

    # Enter the address
    address = input("Enter the location or store name")

    # Store table
    store = pd.read_sql_query (''' select * from stores''', cnxn)
    store = pd.DataFrame(store)

    # Join store branch and store address to get full address
    store_data = store.copy()
    store_data['unit_number'] = store_data['store_branch'].str[0:4]
    store_data['full_address'] = store_data['unit_number'] + ',' + store_data['store_address']

    stores_view_by_location= store_data.loc[store_data['full_address'].str.contains(address, case=False)]
    stores_view_by_location.drop(['store_id'], axis = 1 )
    return stores_view_by_location

# Requirement 4 

def transit_days(transit, orders, vendors, store, vendor):

    # Split data based on space
    df_split = store['store_address'].str.split(' ', expand=True)

    # store name of city in new column
    store['store_location'] = df_split[4]
    
    transit['origin-destination'] = transit['origin'] + "_" + transit['destination']

    order_transit_store = orders.merge(store, on=['store_id'], how = 'inner')
    order_tranit_vendor = order_transit_store.merge(vendors, on = ['vendor_id'], how = 'inner')


    order_transit_intermediate = order_tranit_vendor[['order_id','store_name','store_location','vendor_name','vendor_location']]

    order_transit_intermediate['origin-destination'] = order_transit_intermediate['store_location'] + "_" + order_transit_intermediate['vendor_location']
    order_transit_intermediate = order_transit_intermediate.drop(['store_location','vendor_location'], axis = 1 )

    order_trasnit_final = order_transit_intermediate.merge(transit, on = ['origin-destination'], how='inner')
    order_trasnit_final.drop(['order_id', 'transit_id', 'origin','destination','role_id'], axis =1, inplace = True)

    order_trasnit_final = order_trasnit_final[(order_trasnit_final.vendor_name == vendor)] 
    order_trasnit_final.drop(['vendor_name'], axis=1, inplace = True)
    
    return order_trasnit_final





############################################ RATINGS SUPPLIER ###################################################################

def top_rating_for_store(cnxn):
    StoreNum= input('Enter the store number: ')
    # build up our query string
    query = ("SELECT s.store_name, r.rating, r.ratings_date FROM ratings AS r INNER JOIN stores AS s ON r.store_id = s.store_id"
                    f" WHERE (s.store_id = '{StoreNum}' ) ")

    # execute the query and read to a dataframe in Python
    data = pd.read_sql(query, cnxn)

    return data


