import pandas as pd
import sqlite3

conn = sqlite3.connect("apps.db")

df = pd.read_sql_query("SELECT * FROM apps", conn)

mature_count = df[df["is_mature"] == 1].shape[0]
print("Mature apps:", mature_count)