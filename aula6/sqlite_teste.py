import sqlite3
import pandas as pd

con = sqlite3.connect("sqlite.sqlite")
df = pd.read_sql_query("SELECT * FROM test", con)
print(df)
con.close()