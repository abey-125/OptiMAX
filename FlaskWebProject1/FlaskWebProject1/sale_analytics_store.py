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

#Plotting the graphs
fx_misc.display_maxthreshold_medicine(med_store,med,threshold,store)

#Nikhila Elsa Mathews
#The system shall display a dashboard with minimum threshold of a medicine and current stock on hand
fx_misc.display_minthreshold_medicine(med_store,med,threshold,store)