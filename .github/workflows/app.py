# backend/app.py

from flask import Flask, request, jsonify, render_template
from feedback_store import add_feedback, calculate_average, load_feedback

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_feedback():
    data = request.json
    required = {"name", "subject", "rating", "comments"}

    if not data or not required.issubset(data):
        return jsonify({"error": "Missing fields"}), 400

    if not (1 <= data["rating"] <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    add_feedback(data)
    return jsonify({"message": "Feedback submitted successfully!"}), 200

@app.route("/average", methods=["GET"])
def get_average():
    avg = calculate_average()
    count = len(load_feedback())
    return jsonify({"average_rating": avg, "total": count})

if __name__ == "__main__":
    app.run(debug=True)
