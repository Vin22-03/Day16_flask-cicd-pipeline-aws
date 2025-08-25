from flask import Flask, jsonify, request

app = Flask(__name__)

# Health endpoint for load balancers & smoke tests
@app.get("/health")
def health():
    return jsonify(status="ok"), 200

# Simple Notes API (stub) – we’ll wire a DB later
NOTES = []

@app.get("/api/notes")
def list_notes():
    return jsonify(notes=NOTES), 200

@app.post("/api/notes")
def create_note():
    data = request.get_json(force=True)
    NOTES.append({"id": len(NOTES)+1, "text": data.get("text", "")})
    return jsonify(message="created"), 201

if __name__ == "__main__":
    # Use 0.0.0.0 so Docker can expose it; 8080 for ALB/ECS later
    app.run(host="0.0.0.0", port=8080, debug=True)
