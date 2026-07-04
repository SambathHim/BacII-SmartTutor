import os
import sqlite3
import random
from dotenv import load_dotenv
from google import genai
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chat = client.chats.create(
    model="gemini-2.5-flash"
)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please type a question."}), 400

    try:
        response = chat.send_message(question)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"}), 500


DB_PATH = os.path.join(os.path.dirname(__file__), "questions.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/api/subjects", methods=["GET"])
def get_subjects():
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT subject FROM questions ORDER BY subject"
    ).fetchall()
    conn.close()
    return jsonify({"subjects": [r["subject"] for r in rows]})


@app.route("/api/quiz", methods=["GET"])
def get_quiz():
    subject = request.args.get("subject", "").strip()
    count   = int(request.args.get("count", 5))

    if not subject:
        return jsonify({"error": "subject parameter is required"}), 400

    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM questions WHERE subject = ?", (subject,)
    ).fetchall()
    conn.close()

    if len(rows) < count:
        count = len(rows)

    selected = random.sample(rows, count)

    questions = []
    for q in selected:
        item = {
            "id":       q["id"],
            "type":     q["type"],
            "question": q["question"],
            "answer":   q["answer"],
        }
        if q["type"] == "mcq":
            item["options"] = {
                "A": q["option_a"],
                "B": q["option_b"],
                "C": q["option_c"],
                "D": q["option_d"],
            }
        questions.append(item)

    return jsonify({"subject": subject, "questions": questions})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)