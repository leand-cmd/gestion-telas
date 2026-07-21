import psycopg2

conn = psycopg2.connect('postgresql://postgres:SjUafZYzpKWrXzOpSDgNQISoUGTNTMYw@tokaido.proxy.rlwy.net:44666/railway')
cursor = conn.cursor()
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")

for table in cursor.fetchall():
    print(table[0])

cursor.close()
conn.close()