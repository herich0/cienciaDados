import sqlite3
import pandas as pd

con = sqlite3.connect("sqlite.sqlite")
con.execute("""CREATE TABLE IF NOT EXISTS test (id INTEGER, nome TEXT)""")
con.execute("INSERT INTO test (id,nome) VALUES (1, 'Ana')")
con.execute("INSERT INTO test (id,nome) VALUES (2, 'Bruno')")
con.commit()
cursor = con.execute("SELECT * FROM test")
produtos = cursor.fetchall()
df = pd.DataFrame(produtos, columns=[x[0] for x in cursor.description])
print(df)
con.close()
