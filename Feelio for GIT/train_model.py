import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# -------- Sample Dataset --------
data = {
    "sleep": [2,3,8,7,5,6,1,9,4,6,7,2,8,5],
    "energy": [1,2,4,5,3,4,1,5,2,4,4,1,5,3],
    "stress": [5,4,1,2,3,2,5,1,4,2,2,5,1,3],
    "social": [1,2,4,3,3,4,1,5,2,3,4,1,5,3],
    "positivity": [1,2,5,4,3,4,1,5,2,4,4,1,5,3],
    "mood": [
        "Sad","Sad","Happy","Relaxed","Neutral",
        "Happy","Angry","Happy","Sad","Relaxed",
        "Relaxed","Angry","Happy","Neutral"
    ]
}

df = pd.DataFrame(data)

# -------- Features --------
X = df[["sleep","energy","stress","social","positivity"]]
y = df["mood"]

# -------- Encode Labels --------
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# -------- Train Model --------
model = RandomForestClassifier(random_state=42)
model.fit(X, y_encoded)

# -------- Save Model --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_DIR, "mood_model.pkl"))
joblib.dump(label_encoder, os.path.join(MODEL_DIR, "label_encoder.pkl"))

print("✅ Model trained and saved successfully!")
print("🎯 Classes:", label_encoder.classes_)