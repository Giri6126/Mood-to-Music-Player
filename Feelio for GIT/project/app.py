import os, json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from model_utils import predict_mood_from_answers
from music_player import get_song_for_mood
from quotes import get_quote_for_mood

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    try:
        sleep = float(data.get("sleep", 0) or 0)
        energy = float(data.get("energy", 0) or 0)
        stress = float(data.get("stress", 0) or 0)
        social = float(data.get("social", 0) or 0)
        positivity = float(data.get("positivity", 0) or 0)

        mood = predict_mood_from_answers(
            sleep, energy, stress, social, positivity
        )
    except (ValueError, TypeError, KeyError) as e:
        return jsonify({"error": "Invalid input values. Please ensure all fields are filled with numbers."}), 400

    song_path, song_name = get_song_for_mood(mood)
    quote = get_quote_for_mood(mood)

    # 🔥 IMPORTANT FIX HERE
    song_url = "/" + song_path.replace("\\", "/") if song_path else ""

    return jsonify({
        "mood": mood,
        "song": song_name,
        "song_path": song_url,
        "quote": quote,
        "image": f"/static/images/{mood}.png"
    })

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json

    mood = data["mood"]
    correct = data["correct"]

    os.makedirs("feedback", exist_ok=True)
    path = "feedback/feedback.json"

    feedback_data = []

    if os.path.exists(path):
        with open(path, "r") as f:
            feedback_data = json.load(f)

    feedback_data.append({
        "mood": mood,
        "correct": correct,
        "time": datetime.now().isoformat()
    })

    with open(path, "w") as f:
        json.dump(feedback_data, f, indent=4)

    return jsonify({"message": "✅ Feedback saved!"})

if __name__ == "__main__":
    app.run(debug=True)