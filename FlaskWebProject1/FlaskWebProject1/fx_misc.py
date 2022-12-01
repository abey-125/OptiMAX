# Importing Libraries
import pyodbc
import pandas as pd
import plotly.express as px
from datetime import date, datetime

# Author : Chinnu Treesa Fulton -- Sale analytics for Supplier

def connection():
    # SQL Database Connection
    cnxn_str = ("Driver={SQL Server Native Client 11.0};"
                # Change the server name 
                # Change the server name 
                # Change the server name 
                # Chinnu server : LAPTOP-T8RJOBVC\CFSQL
                # Tony Server : LAPTOP-KUEGS2UO\TSQL
                # Abey Server : MSI\ASQL
                # Nikhila Server : NIKKI-PC\ASQL
                # Amanpreet Server : LAPTOP-BL7HADLT\AKSQL
                "Server=LAPTOP-BL7HADLT\AKSQL;"
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

    most_selling_drug_vendor = df.merge(vendors, on = ['vendor_id'], how = 'inner')
    # Filter to vendor name
    most_selling_drug_vendor = most_selling_drug_vendor[(most_selling_drug_vendor.vendor_name == vendor)] 

    return most_selling_drug_vendor

# Requirement 1

'''Display the most selling drug by store ''' 

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

''' Display most selling drug by time frame'''

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
    color_discrete_sequence =["yellow"])

    # fig.update_xaxes(type='category')
    fig.show()
    return med_count_max_by_Store 

# Requirement 3

''' Display least selling drug by time frame '''

def least_selling_drug_by_time_frame(least_selling_drug_vendor):

    # Enter the time range
    enter_the_date_range_1= input('Enter a 1stdate: ')
    enter_the_date_range_2= input('Enter a 2nddate: ')

    # filtering by time range
    least_selling_drug_by_time = least_selling_drug_vendor[(least_selling_drug_vendor['date_created'] >= enter_the_date_range_1) & (least_selling_drug_vendor['date_created'] <= enter_the_date_range_2)]
    least_selling_drug_by_time.drop(['role_id_x', 'role_id_y'], axis = 1)

    # Viewing the least selling drug
    med_count = least_selling_drug_by_time.groupby(['medicine_name', 'store_id', 'store_name', 'vendor_id', 'vendor_name','date_created']).agg({'quantity' : 'sum'}).rename(columns={'quanity':'medicine_count'}).reset_index()
    # For each store the least selling drug
    med_count_min_by_Store = med_count.groupby(['store_id', 'vendor_id', 'store_name','vendor_name'])['quantity'].min().reset_index()

    med_count_min_by_Store = med_count_min_by_Store.merge(med_count, on  = ['store_id', 'vendor_id', 'store_name', 'quantity', 'vendor_name'], how='inner')
    med_count_min_by_Store = med_count_min_by_Store.drop(['store_id','vendor_id','vendor_name'], axis = 1)
    # Display it as a bar plot
    # x axis has store name and y axis the medicine count
    fig = px.bar(med_count_min_by_Store, x="store_name", y="quantity", text="medicine_name",
    labels={"quantity": "MEDICINE COUNT","store_name": "STORE NAME "}, title="Least Selling Drug from" + " " + enter_the_date_range_1 + " " + "to" + " " + enter_the_date_range_2, 
    color_discrete_sequence =["red"])

    # fig.update_xaxes(type='category')
    fig.show()
    return med_count_min_by_Store

# Requirement 4

''' View stores by location '''

def view_store_by_location(cnxn):

    # Enter the address
    address = input("Enter the location")

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

# Requirement 5 

''' View trasnsit days to different stores'''

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


# Requirement 6

''' View total sales per day '''

def total_sales_per_day(orders, vendors, order_details, vendor):

    # join order and order_details
    order_info = orders.merge(order_details, on = ['order_id', 'role_id'], how = 'inner')
    
    # join with vendor table
    order_vendor = order_info.merge(vendors, on=['vendor_id'], how='inner')

    order_vendor = order_vendor[['vendor_name', 'date_created','quantity', 'unit_price']]
    order_vendor['total'] = order_vendor['quantity'] * order_vendor['unit_price']

    sales_per_day = order_vendor.groupby(['date_created', 'vendor_name']).agg({'total':'sum'}).reset_index()

    sales_per_day['date_created'] = pd.to_datetime(sales_per_day['date_created']).dt.date

    sales_per_day = sales_per_day[(sales_per_day.vendor_name == vendor)] 
    sales_per_day.drop(['vendor_name'], axis=1, inplace = True)

    # Display it as a bar plot
    fig = px.bar(sales_per_day, x="date_created", y="total",
    labels={"date_created": "DATE","total": "TOTAL_SALES"}, title="Total Number of Sales Per Day",
    color_discrete_sequence =["violet"])

    fig.update_xaxes(type='category')
    fig.show()
    
    return sales_per_day

# Requirement 7

''' Display all branches of stores'''

def view_stores(cnxn):

    # Enter the address
    store_name = input("Enter the store name")

    # build up our query string
    query = ("SELECT store_name, store_branch, store_address, store_contact, store_email FROM stores"
                    f" WHERE (store_name = '{store_name}' ) ")

    # execute the query and read to a dataframe in Python
    data = pd.read_sql(query, cnxn)

    return data


# Requirement 8

''' Display sale of individual store'''

def total_sales_stores(orders, vendors, order_details, vendor, store):
    
    # join order and order_details
    order_info = orders.merge(order_details, on = ['order_id', 'role_id'], how = 'inner')
    order_info.head()

    # join with vendor table
    order_vendor = order_info.merge(vendors, on=['vendor_id'], how='inner')

    # Join with store table
    order_vendor_store = order_vendor.merge(store, on=['store_id'], how='inner')

    # Select needed columns
    order_vendor_store = order_vendor_store[['vendor_name', 'store_name', 'store_branch', 'quantity', 'unit_price']]

    # total = quanitity * unit_price
    order_vendor_store['total'] = order_vendor_store['quantity'] * order_vendor_store['unit_price']

    # group by store name and branch
    sales_per_store = order_vendor_store.groupby(['store_name','store_branch','vendor_name']).agg({'total':'sum'}).reset_index()

    sales_per_store = sales_per_store[(sales_per_store.vendor_name == vendor)] 
    sales_per_store.drop(['vendor_name'], axis=1, inplace = True)

    # Display it as a bar plot
    fig = px.bar(sales_per_store, x="store_name", y="total",
    labels={"store_name": "STORE_NAME","total": "TOTAL_SALES"}, title="Total Sales for Store",
    color_discrete_sequence =["blue"])

    fig.update_xaxes(type='category')
    fig.show()

    sales_per_store.head()


# Requirement 9

''' Display sale of all branches combined'''

def total_sales_branches(orders, vendors, order_details, vendor, store):
    
    # join order and order_details
    order_info = orders.merge(order_details, on = ['order_id', 'role_id'], how = 'inner')
    order_info.head()

    # join with vendor table
    order_vendor = order_info.merge(vendors, on=['vendor_id'], how='inner')

    # Join with store table
    order_vendor_store = order_vendor.merge(store, on=['store_id'], how='inner')

    # Select needed columns
    order_vendor_store = order_vendor_store[['vendor_name', 'store_name', 'store_branch', 'quantity', 'unit_price']]

    # total = quanitity * unit_price
    order_vendor_store['total'] = order_vendor_store['quantity'] * order_vendor_store['unit_price']

    # group by store name and branch
    sales_per_store = order_vendor_store.groupby(['store_name','vendor_name']).agg({'total':'sum'}).reset_index()

    sales_per_store = sales_per_store[(sales_per_store.vendor_name == vendor)] 
    sales_per_store.drop(['vendor_name'], axis=1, inplace = True)

    # Display it as a bar plot
    fig = px.bar(sales_per_store, x="store_name", y="total",
    labels={"store_name": "STORE_NAME","total": "TOTAL_SALES"}, title="Total Sales for all Branches of Store",
    color_discrete_sequence =["green"])

    fig.update_xaxes(type='category')
    fig.show()

    return sales_per_store.head()




############################################ RATINGS SUPPLIER ###################################################################
# NAMA SCRIPT BEGIN 


def top_rating_for_store(cnxn):
    StoreNum= input('Enter the store number: ')
    # build up our query string
    query = ("SELECT TOP 5 s.store_name, r.rating, r.ratings_date FROM ratings AS r INNER JOIN stores AS s ON r.store_id = s.store_id"
                    f" WHERE (s.store_id = '{StoreNum}' ) ")

    # execute the query and read to a dataframe in Python
    data = pd.read_sql(query, cnxn)

    return data

def top_review_for_store(cnxn):
    StoreNum= input('Enter the store number: ')
    # build up our query string
    query = ("SELECT TOP 5 s.store_name, r.review_comment, r.ratings_date FROM ratings AS r INNER JOIN stores AS s ON r.store_id = s.store_id"
                    f" WHERE (s.store_id = '{StoreNum}' ) ")

    # execute the query and read to a dataframe in Python
    data = pd.read_sql(query, cnxn)

    return data


############################################ STORES ###################################################################

# display the transit days between two stores
def display_transit_days(cnxn):
    Store1 = input('Enter the origin store id: ')
    Store2 = input('Enter the destination store id:')
    query = ("SELECT s1.store_name , origin, s2.store_name, destination, days"
             f" FROM transit_days t , stores s1, stores s2"
             f" WHERE origin = s1.city AND destination = s2.city"
             f" AND s1.store_id = '{Store1}' AND s2.store_id = '{Store2}';" )
    data = pd.read_sql(query, cnxn)
    return data

# display medicines to stores which have SOH less than the min threshold 
def display_med_SOH_less_min(cnxn):
    query = ("SELECT s.store_name, m.medicine_name, ms.stock_in_hand, mt.min_threshold, mt.max_threshold"
             f" FROM medicines AS m INNER JOIN"
             f" med_store AS ms ON m.medicine_id = ms.medicine_id INNER JOIN"
             f" stores AS s ON ms.store_id = s.store_id INNER JOIN"
             f" med_threshold AS mt ON m.medicine_id = mt.medicine_id AND ms.stock_in_hand < mt.min_threshold")
    data = pd.read_sql(query, cnxn)
    return data

#creating new orders
def create_new_order(cnxn):
    query = ("select max(order_id) + 1 AS max_order_id from orders;")
    max_order_id = pd.read_sql_query(query, cnxn)
    max_order_id = pd.DataFrame(max_order_id, columns = ['max_order_id'])
    #max_order_id = max_order_id.astype({'max_order_id':'int'})
    print(max_order_id)
    med = int(input('Enter the medicine id: '))
    ven = int(input('Enter the vendor id: '))
    print(ven)
    store = int(input('Enter the store id: '))
    print(store)
    qty = int(input('Enter the quantity:'))
    price= (" SELECT m.standard_price + me.freight_amount AS price"
            f" FROM medicines AS m INNER JOIN"
            f" medicine_expense AS me ON m.medicine_id = me.medicine_id"
            f" WHERE (m.medicine_id = {med})")
    data = pd.read_sql_query (price, cnxn)
    price = pd.DataFrame(data, columns = ['price'])
    price = price.astype({'price':'int'})
    print(price)
    total_price = price['price'] * qty
    total_price= int(total_price)
    now = datetime.now()
    print(now)

    cursor = cnxn.cursor()
    for index, row in max_order_id.iterrows(): 
        add_order = ("INSERT INTO orders "
                        f" (order_id,vendor_id,store_id,date_created,order_status,total_price,role_id) "
                        f" VALUES (?,?,?,?,?,?,?)")
        data_order = (int(row.max_order_id), ven, store, now, 'S', total_price, 1)
        cursor.execute(add_order, data_order)
        print("Order Created Successfully")
    cnxn.commit()

# display medicines to stores which have SOH more than the max threshold 
def display_med_SOH_more_max(cnxn):
    query = ("SELECT s.store_name, m.medicine_name, ms.stock_in_hand, mt.min_threshold, mt.max_threshold"
             f" FROM medicines AS m INNER JOIN"
             f" med_store AS ms ON m.medicine_id = ms.medicine_id INNER JOIN"
             f" stores AS s ON ms.store_id = s.store_id INNER JOIN"
             f" med_threshold AS mt ON m.medicine_id = mt.medicine_id AND ms.stock_in_hand > mt.max_threshold")
    data = pd.read_sql(query, cnxn)
    return data


#creating new return
def create_new_return(cnxn):
    query = ("select max(return_id) + 1 AS max_return_id from ord_returns;")
    max_return_id = pd.read_sql_query(query, cnxn)
    max_return_id = pd.DataFrame(max_return_id, columns = ['max_return_id'])
    #max_return_id = max_return_id.astype({'max_return_id':'int'})
    print(max_return_id)
    med = int(input('Enter the medicine id: '))
    ven = int(input('Enter the vendor id: '))
    print(ven)
    store = int(input('Enter the store id: '))
    print(store)
    qty = int(input('Enter the quantity:'))
    price= (" SELECT m.standard_price + me.freight_amount AS price"
            f" FROM medicines AS m INNER JOIN"
            f" medicine_expense AS me ON m.medicine_id = me.medicine_id"
            f" WHERE (m.medicine_id = {med})")
    data = pd.read_sql_query (price, cnxn)
    price = pd.DataFrame(data, columns = ['price'])
    price = price.astype({'price':'int'})
    print(price)
    total_price = price['price'] * qty
    total_price= int(total_price)
    now = datetime.now()
    print(now)

    cursor = cnxn.cursor()
    for index, row in max_return_id.iterrows(): 
        add_return = ("INSERT INTO ord_returns "
                        f" (return_id,vendor_id,store_id,total_price,returned_date,role_id) "
                        f" VALUES (?,?,?,?,?,?)")
        data_return = (int(row.max_return_id), ven, store, total_price,now, 1)
        cursor.execute(add_return, data_return)
        print("Return Created Successfully")
    cnxn.commit()

def disply_expired_meds(cnxn):
    now = datetime.now()
    # build up our query string
    query = ("SELECT medicine_id, medicine_name, expiry_date, manufactured_date, medicine_type, key_ingredient, standard_price, role_id"
             f" FROM     medicines"
             f" WHERE  (expiry_date <= '{now}')")
    # execute the query and read to a dataframe in Python
    data = pd.read_sql(query, cnxn)
    return data


############################################ NAMA SCRIPT END #################################################################################

############################# SALE ANALYTICS STORE ####################################################

# Nikhila Elsa Mathews
# The system shall display a default threshold for each medicine based on its sales

def display_maxthreshold_medicine(med_store,med,threshold,store):
    
    #Joining various tables
    innerjoin1 = med_store.merge(threshold, on = ['store_id','medicine_id','role_id'], how = 'inner')
    innerjoin1=innerjoin1.merge(med_store,on=['medicine_id','role_id','store_id','stock_in_hand','transit_quantity'],how='inner')
    innerjoin2 = innerjoin1.merge(med, on = ['medicine_id','role_id'], how = 'inner')
    innerjoin3=innerjoin2.merge(store, on=['store_id','role_id'],how='inner')
    #Plotting the graphs
    threshold_graph = pd.melt(innerjoin3, id_vars=['medicine_name', 'store_name' ], \
    value_vars =['max_threshold','stock_in_hand'
    ], var_name='Inventory', value_name='Values')

    threshold_graph=threshold_graph.groupby(['medicine_name','store_name','Inventory']).agg({'Values' : 'sum'}).sort_values(by='Values').reset_index()

    fig = px.bar(threshold_graph, x="medicine_name", y="Values", color="Inventory")
    fig.show()
	
 # Nikhila Elsa Mathews
 # The system shall display a dashboard with minimum threshold of a medicine and current stock on hand

def display_minthreshold_medicine(med_store,med,threshold,store):
    
    #Joining various tables
    innerjoin1 = med_store.merge(threshold, on = ['store_id','medicine_id','role_id'], how = 'inner')
    innerjoin1=innerjoin1.merge(med_store,on=['medicine_id','role_id','store_id','stock_in_hand','transit_quantity'],how='inner')
    innerjoin2 = innerjoin1.merge(med, on = ['medicine_id','role_id'], how = 'inner')
    innerjoin3=innerjoin2.merge(store, on=['store_id','role_id'],how='inner')
    #Plotting the graphs
    threshold_graph = pd.melt(innerjoin3, id_vars=['medicine_name', 'store_name' ], \
    value_vars =['min_threshold','stock_in_hand'
    ], var_name='Inventory', value_name='Values')

    threshold_graph=threshold_graph.groupby(['medicine_name','store_name','Inventory']).agg({'Values' : 'sum'}).sort_values(by='Values').reset_index()

    fig = px.bar(threshold_graph, x="medicine_name", y="Values", color="Inventory")
    fig.show()
