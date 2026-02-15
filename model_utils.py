import joblib
import numpy as np

model = joblib.load("mood_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

def predict_mood_from_answers(sleep, energy, stress, social, positivity):
    X = np.array([[sleep, energy, stress, social, positivity]])
    pred = model.predict(X)
    mood = label_encoder.inverse_transform(pred)[0]
    return mood
