from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from fuzzywuzzy import fuzz
from textblob import TextBlob

# --- Load chat data ---
DATA_FILE = "chat.json"
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

app = Flask(__name__)
CORS(app)  # allows connection from your frontend (home.html)

# --- Basic helper functions from Kenny ---
def normalize_input(user_input):
    synonym_map = {
        "hi": ["hello", "hey", "yo", "sup", "wsg", "wassup"],
        "how are you": ["how's it going", "how are ya", "how you doing", "what's up", "how r u", "how r you", "how are u", "how u doing"],
        "goodbye": ["bye", "goodbye", "later", "cya", "see ya", "gtg", "gotta go"],
        "help": ["can you help me", "i need help", "assist me", "help me out", "can u help me", "need help", "help pls", "help"],
        "you": ["u", "ya"],
        "are": ["r"],
        "okay": ["ok", "k", "alr", "aight", "ight"],
        "nothing": ["nothin", "nun"],
        "yes": ["ye", "yea", "yeah", "yep", "yh", "affirmative", "sure"],
        "no": ["nah", "nope", "nuh uh"],
        "thanks": ["thank you", "thx", "ty", "tysm", "thanx"],
        "what": ["wat", "wut", "wht"],
        "because": ["cuz", "cos", "bc", "cause"]
    }
    user_input = user_input.lower()
    words = user_input.split()
    normalized_words = []
    for word in words:
        replaced = False
        for key, synonyms in synonym_map.items():
            if word in synonyms:
                normalized_words.append(key)
                replaced = True
                break
        if not replaced:
            normalized_words.append(word)
    return " ".join(normalized_words)

def get_best_match(user_input):
    max_score = 0
    best_match = None
    for entry in data:
        score = fuzz.ratio(user_input.strip().lower(), entry["prompt"].strip().lower())
        if score > max_score:
            max_score = score
            best_match = entry
    return best_match, max_score

# --- Flask route ---
@app.route("/chat", methods=["POST"])
def chat():
    message = request.get_json().get("message", "")
    normalized = normalize_input(message)
    best_match, score = get_best_match(normalized)

    if best_match and score >= 60:
        reply = best_match["response"]
    else:
        reply = "Sorry, I don't understand that."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

