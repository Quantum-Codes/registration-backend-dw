import os
import pymysql
from flask import Flask, request, send_file

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "users_db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))


def get_db():
    connect_kwargs = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME,
        "port": DB_PORT,
        "autocommit": True,
    }
    if os.getenv("DB_SSL", "false").lower() == "true":
        connect_kwargs["ssl"] = {"ssl_mode": "REQUIRED"}

    return pymysql.connect(**connect_kwargs)


def init_db():
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    password VARCHAR(255)
                )
            """)
        conn.close()
        print("Database connected and table verified!")
    except Exception as e:
        print(f"DB init warning (check environment variables if unconfigured): {e}")


init_db()


@app.route("/")
def index():
    return send_file("static/index.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password),
        )
    conn.close()

    return "Registration successful!"


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
