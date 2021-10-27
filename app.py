from flask import Flask, render_template, redirect, request
import psycopg2
from dotenv import load_dotenv
import os
from secrets import choice
from string import ascii_uppercase, ascii_lowercase
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/api/original")
def original():
    return redirect("/")

def generate_url():
    length = 7
    return ''.join([choice(ascii_uppercase + ascii_lowercase) for char in range(length)])

@app.route("/api/shorten", methods=["POST"])
def shorten():

    # Supports both JSON and urlencoded.
    data = request.json
    if data == None:
        data = request.form

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    print(data)

    db = conn.cursor()
    new = generate_url()
    original = data["url"]
    print(original)
    print(new)
    db.execute("INSERT INTO urls (new, original) VALUES (%s, %s)", (new, original))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)