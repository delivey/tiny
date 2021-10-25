import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="q"
)

db = conn.cursor()

db.execute(
"""
CREATE TABLE IF NOT EXISTS urls (
    original VARCHAR(255) NOT NULL,
    new VARCHAR(25) NOT NULL
)
"""
)
print("'urls' table created!")

conn.commit()
conn.close()