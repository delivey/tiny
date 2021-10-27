from flask import Flask, render_template, redirect, request, jsonify
import psycopg2
from dotenv import load_dotenv
import os
from secrets import choice
from string import ascii_uppercase, ascii_lowercase
load_dotenv()

app = Flask(__name__)

# Returns an url code.
def generate_url():
    length = 6
    return "u" + ''.join([choice(ascii_uppercase + ascii_lowercase) for _ in range(length)])

def get_url_from_code(code):
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    db = conn.cursor()

    db.execute("SELECT original FROM urls WHERE new=%s", ("u"+code,))
    original = db.fetchone()[0]
    conn.close()
    return original

# Routes for demo
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/u<code>", methods=["GET"])
def get(code):
    url = get_url_from_code(code)
    return redirect(url)

# Routes for API
@app.route("/api/original")
def original():
    code = request.json.code
    url = get_url_from_code(code)
    return jsonify({"url": url})

@app.route("/api/shorten", methods=["POST"])
def shorten():

    # Supports both JSON and urlencoded (required for demo)
    data = request.json
    if data == None: data = request.form

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    db = conn.cursor()

    new = generate_url()
    original = data["url"]

    db.execute("INSERT INTO urls (new, original) VALUES (%s, %s)", (new, original))

    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)