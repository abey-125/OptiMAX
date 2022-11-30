# Importing Libraries
import pyodbc
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import fx_misc
import warnings
warnings.filterwarnings("ignore")

######################################### MENU DRIVEN PROGRAM ###########################################

# Connection string
cnxn = fx_misc.connection()

# Importing tables

# transit days table
transit = pd.read_sql_query (''' select * from transit_days''', cnxn)
transit = pd.DataFrame(transit)

# Store table
store = pd.read_sql_query (''' select * from stores''', cnxn)
store = pd.DataFrame(store)

# orders table
orders = pd.read_sql_query (''' select * from orders''', cnxn)
orders = pd.DataFrame(orders)

# vendor table
vendors = pd.read_sql_query (''' select * from vendors''', cnxn)
vendors = pd.DataFrame(vendors)

# orders details Table
order_details = pd.read_sql_query (''' select * from order_details''', cnxn)
order_details = pd.DataFrame(order_details)

# printing the starting line  
print("OPTIMAX")  
  
# creating options  
while True:  
    print("\n OPTIONS")  
    print("1. Supplier")  
    print("2. Store")  
    print("3. Log Out")  
    choice1 = int(input("Enter the Choice:"))  
  
    if choice1 == 1:  
        # Enter the vendor name as input
        vendor = input("Enter the vendor name")
        medicine_order = fx_misc.most_selling_drug_preprocessing(cnxn)
        selling_drug_vendor = fx_misc.filter_vendor_name(vendor, medicine_order, cnxn)

        while True:
            print("1. SALE ANALYTICS SUPPLIER")  
            print("2. REVIEW / RATES")  
            print("3. COMPARISON")  
            print("4. Exit")  
            choice2 = int(input("Enter the Choice:"))  

            while True:
                if choice2 == 1:  
                    print("1. VIEW STORES BY LOCATION")  
                    print("2. VIEW MOST SELLING DRUG")  
                    print("3. VIEW MOST SELLING DRUG BY TIME FRAME")  
                    print("4. VIEW LEAST SELLING DRUG BY TIME FRAME")  
                    print("5. TRANSIT DAYS")  
                    print("6. TOTAL NUMBER OF SALES PER DAY")  
                    print("7. SALE OF INDIVIDUAL STORE")  
                    print("8. DISPLAY ALL BRANCHES")
                    print("9. SALE OF ALL BRANCHES COMBINED")
                    print("10. Exit")
                    choice3 = int(input("Enter the Choice:"))

                    if choice3 == 1:
                        print(fx_misc.view_store_by_location(cnxn))
                    if choice3 == 2:
                        print(fx_misc.most_selling_drug(selling_drug_vendor))
                    if choice3 == 3:
                        print(fx_misc.most_selling_drug_by_time_frame(selling_drug_vendor))
                    if choice3 == 4:
                        print(fx_misc.least_selling_drug_by_time_frame(selling_drug_vendor))
                    if choice3 == 5:
                        print(fx_misc.transit_days(transit, orders, vendors, store, vendor))
                    if choice3 == 6:
                        print(fx_misc.total_sales_per_day(orders, vendors, order_details, vendor))
                    if choice3 == 7:
                        print(fx_misc.total_sales_stores(orders, vendors, order_details, vendor, store))
                    if choice3 == 8:
                        print(fx_misc.view_stores(cnxn))
                    if choice3 == 9:
                        print(fx_misc.total_sales_branches(orders, vendors, order_details, vendor, store))
                    if choice3 == 10:
                        break           
                
                elif choice2 == 2: 
                    # Review / Rates
                    while True:
                        print("1. DISPLAY TOP 5 RATES") 
                        print("2. EXIT")
                        choice2_1 =  int(input("Enter the Choice:"))
                        
                        if choice2_1 == 1:
                            print(fx_misc.top_rating_for_store(cnxn))

                        if choice2_1 == 2:
                            break
                        
                elif choice2 == 3: 
                    # Comparison 
                    print("1.DISPLAY TOP 5 RATES")   
                    
                elif choice2 == 4:  
                    break  
                    
                else:  
                    print("Oops! Incorrect Choice.")  

    elif choice1 == 2:  
        # Store analytics 
        print("1. ")  
        print("2. ")  
        print("3. ")  
        print("4. ")  
        choice3 = int(input("Enter the Choice3:"))  

        if choice3 == 1:  
            radius = int(input("Enter Radius of Circle:"))  
            
            
        elif choice3 == 2:  
            height = int(input("Enter Height of Rectangle:"))  
            width = int(input("Enter Width of Rectangle:"))  
            
            
        elif choice3 == 3:  
            side = int(input("Enter Side of Square:"))  
            

        elif choice3 == 4:  
            break  
            
        else:  
            print("Oops! Incorrect Choice.")  

    elif choice1 == 3:  
        break  

    else:  
        print("Oops! Incorrect Choice.")  


