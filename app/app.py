import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app_pw@localhost:5432/app_staging")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/users")
def list_users():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, COALESCE(email, '') FROM users ORDER BY id")
            rows = cur.fetchall()
            users = [{"id": r[0], "username": r[1], "email": r[2]} for r in rows]
    return jsonify(users)

@app.post("/users")
def add_user():
    data = request.get_json(force=True)
    username = data.get("username")
    email = data.get("email")
    if not username:
        return {"error": "username is required"}, 400
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id",
                (username, email)
            )
            new_id = cur.fetchone()[0]
    return {"id": new_id, "username": username, "email": email}, 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
