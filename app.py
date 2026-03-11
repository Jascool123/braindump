from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import json

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/organize", methods=["POST"])
def organize():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You organize brain dumps into 4 categories. Return ONLY valid JSON with this exact structure, no other text:
{"tasks":[],"notes":[],"reminders":[],"ideas":[]}

Rules:
- tasks = actionable things to do
- notes = information to remember
- reminders = time-sensitive things
- ideas = creative thoughts or concepts
- Each item max 1 sentence
- Empty array if nothing fits that category
- ONLY return the JSON, nothing else"""
            },
            {
                "role": "user",
                "content": f"Organize this brain dump:\n\n{text}"
            }
        ]
    )

    raw = response.choices[0].message.content.strip().replace("```json", "").replace("```", "").strip()
    parsed = json.loads(raw)
    return jsonify(parsed)


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "BrainDump API is running!"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
