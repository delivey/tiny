import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DATABASE"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
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