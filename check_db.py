import sqlite3
conn = sqlite3.connect('e:/project/IBM_Hackathon/data/chatops.db')
cursor = conn.cursor()
cursor.execute('SELECT id, role, content FROM messages ORDER BY timestamp DESC LIMIT 10')
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r[0]}, Role: {r[1]}, Content: {repr(r[2])}")
conn.close()
