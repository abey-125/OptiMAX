import plotly.express as px
import matplotlib.pyplot as plt
import plotly.io as pio
import pandas as pd
import fx_misc
# SQL Database Connection
cnxn=fx_misc.connection()

#The system shall display a default threshold for each medicine based on its sales:Nikhila Elsa Mathews
#Fetching values needed from the corresponding tables
med_store = pd.read_sql_query (''' select * from med_store''', cnxn)
med_store = pd.DataFrame(med_store)
med_store

med = pd.read_sql_query (''' select * from medicines''', cnxn)
med = pd.DataFrame(med)
med

threshold=pd.read_sql_query (''' select * from med_threshold''', cnxn)
threshold = pd.DataFrame(threshold)
threshold

store = pd.read_sql_query (''' select * from stores''', cnxn)
store = pd.DataFrame(store)
store

#Joining various tables
innerjoin1 = med_store.merge(threshold, on = ['store_id','medicine_id','role_id'], how = 'inner')
innerjoin1=innerjoin1.merge(med_store,on=['medicine_id','role_id','store_id','stock_in_hand','transit_quantity'],how='inner')
innerjoin2 = innerjoin1.merge(med, on = ['medicine_id','role_id'], how = 'inner')
innerjoin3=innerjoin2.merge(store, on=['store_id','role_id'],how='inner')
#Plotting the graphs
fx_misc.display_maxthreshold_medicine(cnxn,innerjoin3)

#Nikhila Elsa Mathews
#The system shall display a dashboard with minimum threshold of a medicine and current stock on hand
fx_misc.display_minthreshold_medicine(cnxn,innerjoin3)