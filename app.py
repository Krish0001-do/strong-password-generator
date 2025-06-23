from flask import Flask, render_template, request, jsonify
import random
import string
import re

app = Flask(__name__)

# 🔧 Function to generate password
def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_upper else ''
    digits = string.digits if use_digits else ''
    symbols = string.punctuation if use_symbols else ''
    all_chars = lower + upper + digits + symbols
    if not all_chars:
        return ""
    return ''.join(random.choice(all_chars) for _ in range(length))

# ✅ Strength Checker
def check_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\\[\]]", password): score += 1

    if score == 5:
        return "Strong"
    elif 3 <= score < 5:
        return "Medium"
    else:
        return "Weak"

# 💪 Function to make any password stronger
def make_stronger(base_pw):
    base_pw += ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=6))

    # Force at least one of each type
    if not re.search(r"[A-Z]", base_pw):
        base_pw += random.choice(string.ascii_uppercase)
    if not re.search(r"[a-z]", base_pw):
        base_pw += random.choice(string.ascii_lowercase)
    if not re.search(r"\d", base_pw):
        base_pw += random.choice(string.digits)
    if not re.search(r"[!@#$%^&*]", base_pw):
        base_pw += random.choice("!@#$%^&*")

    # Ensure length >= 12
    while len(base_pw) < 12:
        base_pw += random.choice(string.ascii_letters + string.digits + "!@#$%^&*")

    # Final shuffle
    return ''.join(random.sample(base_pw, len(base_pw)))


# 🔁 Generate suggestions from modified password
def generate_suggestions(base_pw, count=3):
    return [make_stronger(base_pw) for _ in range(count)]

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    password = generate_password(
        length=int(data.get("length", 12)),
        use_upper=data.get("upper", True),
        use_digits=data.get("digits", True),
        use_symbols=data.get("symbols", True)
    )
    strength = check_strength(password)
    return jsonify({"password": password, "strength": strength})

@app.route("/check", methods=["POST"])
def check():
    pw = request.json.get("password", "")
    return jsonify({"strength": check_strength(pw)})

@app.route("/suggest", methods=["POST"])
def suggest():
    base_pw = request.json.get("base_pw", "")
    suggestions = generate_suggestions(base_pw)
    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True)
