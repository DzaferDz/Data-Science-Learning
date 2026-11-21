import sqlite3
import pandas as pd

conn = sqlite3.connect('fifa20.db')
df = pd.read_csv('players_20.csv')
df.to_sql('players_20', conn, if_exists='replace', index=False)
print("Loaded 18,278 players into fifa20.db")

cur = conn.cursor()
cur.execute("SELECT short_name, club, age, overall, potential FROM players_20 WHERE age <= 21 AND potential >= 88 ORDER BY potential DESC LIMIT 3")
print("Query 1:", cur.fetchall())

cur.execute("""
SELECT club, COUNT(sofifa_id), ROUND(AVG(overall), 1), SUM(value_eur), SUM(wage_eur)
FROM players_20
WHERE club IS NOT NULL AND club != ''
GROUP BY club
ORDER BY SUM(value_eur) DESC LIMIT 3
""")
print("Query 2:", cur.fetchall())
conn.close()
