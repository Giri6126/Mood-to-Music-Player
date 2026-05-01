 Feelio — Music that understands you.

Feelio is an AI-powered mood-based music recommendation web application that understands your emotions and plays the perfect song for your current state of mind.

---

## 🚀 Features

* 🎯 Mood prediction using Machine Learning
* 🎵 Automatic music recommendation based on mood
* 🎨 Modern UI with glassmorphism design
* 🌈 Dynamic themes based on mood
* 🎧 Custom music player with controls
* 📊 Real-time audio visualizer
* 👍 Feedback system (Like / Dislike)
* ⚡ Smooth and responsive user experience

---

## 🧠 How It Works

1. User fills out a short questionnaire:

   * Sleep
   * Energy
   * Stress
   * Social
   * Positivity

2. Data is sent to the Flask backend

3. A **Random Forest Classifier** predicts the mood

4. Based on the mood:

   * A song is selected
   * UI updates dynamically
   * Music starts playing

---

## 🏗️ Tech Stack

**Frontend:**

* HTML
* CSS
* JavaScript

**Backend:**

* Flask (Python)

**Machine Learning:**

* Random Forest Classifier (Scikit-learn)

---

## 📁 Project Structure

```
Feelio/
│
├── app.py
├── model_utils.py
├── music_player.py
│
├── models/
│   ├── mood_model.pkl
│   └── label_encoder.pkl
│
├── static/
│   ├── music/          # (Not included - see note below)
│   ├── images/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── feedback/
│   └── feedback.json
│
└── README.md
```

---

## ⚠️ Note on Music Files

Music files are **not included** in this repository due to copyright restrictions.

To run the project:

1. Add your own `.mp3` files inside:

```
static/music/<mood>/
```

Example:

```
static/music/happy/
static/music/sad/
```

---

## ▶️ How to Run Locally

1. Clone the repository:

```
git clone https://github.com/your-username/feelio.git
cd feelio
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the Flask app:

```
python app.py
```

4. Open in browser:

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

> Add screenshots of:

* Questionnaire UI
* Song player UI
* Visualizer

---

## 🔮 Future Enhancements

* 🎤 Voice-based mood input
* 📱 Mobile app version
* 📡 GPS-based context-aware recommendations
* 🤖 Adaptive learning from user feedback

---

## 💡 Inspiration

Sometimes music understands us better than people.
Feelio aims to bridge emotion and sound using AI.

---

## 👨‍💻 Author

* Your Name
* Rajalakshmi Institute of Technology
* B.E CSE (AIML)

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub and share your feedback!

---

## 🧠 Final Note

> “Feelio doesn’t just play music — it understands you.”
