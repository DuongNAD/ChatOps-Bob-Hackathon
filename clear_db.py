import sqlite3
conn = sqlite3.connect('e:/project/IBM_Hackathon/data/chatops.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM messages WHERE session_id = 'tg_8214043955'")
conn.commit()
print(f"Deleted {cursor.rowcount} messages from history.")
conn.close()
