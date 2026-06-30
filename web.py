import json
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Each form submission is appended here, one JSON object per line.
SUBMISSIONS_FILE = Path(__file__).parent / "submissions.jsonl"


@app.route("/")
def home():
    # Renders templates/index.html
    return render_template("index.html")


@app.route("/consult", methods=["POST"])
def consult():
    """Receive a 'Hire AI Developers' contact request and save it."""
    # Accept JSON (from the page's fetch call) or a normal form POST.
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    company = (data.get("company") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email:
        return jsonify(status="error", message="Name and email are required."), 400

    record = {
        "received_at": datetime.now().isoformat(timespec="seconds"),
        "name": name,
        "email": email,
        "company": company,
        "message": message,
    }
    with SUBMISSIONS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    # Also print to the console so you can see requests live while developing.
    print(f"[consult] new request from {name} <{email}>")

    return jsonify(status="ok", message="Thanks! We'll be in touch shortly.")


if __name__ == "__main__":
    # debug=True auto-reloads on file changes while developing
    app.run(host="127.0.0.1", port=8000, debug=True)
