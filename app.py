from flask import Flask, jsonify, request, render_template_string
import psycopg2
import os

app = Flask(__name__)

# Get DB credentials from env vars
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME", "notesdb")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "5432")


# Connect to the RDS PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn


# 🎨 Beautiful Homepage with CI/CD Info
@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>VinCloudOps 🚀</title>
        <style>
            body {
                background: linear-gradient(to right, #1e3c72, #2a5298);
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                padding-top: 10%;
            }
            .container {
                background-color: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
                display: inline-block;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 10px;
            }
            p {
                font-size: 1.5em;
                margin-top: 0;
                font-weight: 300;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Vin’s Cloud-Powered Notes API</h1>
            <p>Deployed with 💻 <strong>Jenkins + Docker + Terraform + ECS + ALB</strong></p>
            <p>Built by a Fresher, Ready for Production 🚀</p>
        </div>
    </body>
    </html>
    """)

# ✅ Health endpoint for ALB health checks
@app.get("/health")
def health():
    return jsonify(status="ok"), 200

# Create notes table if it doesn't exist
@app.before_first_request
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# ✅ GET all notes from RDS
@app.route("/api/notes", methods=["GET"])
def list_notes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM notes;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    notes = [{"id": r[0], "text": r[1]} for r in rows]
    return jsonify(notes=notes), 200


# ✅ POST a new note to RDS
@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json(force=True)
    text = data.get("text", "")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (text) VALUES (%s);", (text,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(message="created"), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
