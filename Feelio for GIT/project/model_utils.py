import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "mood_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)


def predict_mood_from_answers(sleep, energy, stress, social, positivity):
    X = np.array([[sleep, energy, stress, social, positivity]])
    prediction = model.predict(X)
    mood = label_encoder.inverse_transform(prediction)[0]
    return mood