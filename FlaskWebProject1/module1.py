import pyodbc




connection_String="MSI\ASQL;Initial Catalog=Messy;Integrated Security=True"
cnxn = pyodbc.connect(connection_String)