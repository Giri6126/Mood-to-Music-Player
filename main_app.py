import customtkinter as ctk
from PIL import Image
import os, json
from datetime import datetime

from model_utils import predict_mood_from_answers
from music_player import get_song_for_mood, play_song, stop_song

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MoodMusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mood to Music Player")
        self.geometry("450x650")
        self.resizable(False, False)

        self.inputs = {}

        self.build_questionnaire()

    # ---------------- Questionnaire ----------------
    def build_questionnaire(self):
        ctk.CTkLabel(self, text="🎵 Mood to Music Player",
                     font=("Segoe UI", 22, "bold")).pack(pady=20)

        self.inputs["sleep"] = self.add_question("Sleep hours (0–10)")
        self.inputs["energy"] = self.add_question("Energy level (1–5)")
        self.inputs["stress"] = self.add_question("Stress level (1–5)")
        self.inputs["social"] = self.add_question("Social activity (1–5)")
        self.inputs["positivity"] = self.add_question("Positivity level (1–5)")

        ctk.CTkButton(
            self,
            text="🎯 Predict Mood",
            height=40,
            command=self.predict_and_play
        ).pack(pady=30)

    def add_question(self, text):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=8)

        ctk.CTkLabel(frame, text=text, width=260, anchor="w").pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame, width=80)
        entry.pack(side="right", padx=10)
        return entry

    # ---------------- Mood Result ----------------
    def predict_and_play(self):
        stop_song()

        values = [float(self.inputs[k].get()) for k in self.inputs]
        mood = predict_mood_from_answers(*values)

        for widget in self.winfo_children():
            widget.destroy()

        self.show_result(mood)

    # ---------------- Result Screen ----------------
    def show_result(self, mood):
        ctk.CTkLabel(
            self,
            text=f"Predicted Mood: {mood}",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        img_path = f"images/{mood}.png"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = ctk.CTkImage(light_image=img, size=(220, 220))
            label = ctk.CTkLabel(self, image=img, text="")
            label.image = img
            label.pack(pady=10)

        song_path, song_name = get_song_for_mood(mood)
        if song_path:
            play_song(song_path)
            ctk.CTkLabel(self, text=f"🎶 Now Playing: {song_name}").pack(pady=10)

        self.feedback_buttons(mood)

    # ---------------- Feedback ----------------
    def feedback_buttons(self, mood):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20)

        ctk.CTkButton(
            frame, text="👍 Yes",
            command=lambda: self.save_feedback(mood, True)
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            frame, text="👎 No",
            command=lambda: self.save_feedback(mood, False)
        ).grid(row=0, column=1, padx=10)

    def save_feedback(self, mood, correct):
        os.makedirs("feedback", exist_ok=True)
        path = "feedback/feedback.json"

        data = []
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)

        data.append({
            "mood": mood,
            "correct": correct,
            "time": datetime.now().isoformat()
        })

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        ctk.CTkLabel(self, text="✅ Feedback saved. Thank you!").pack(pady=10)


# ---------------- Run App ----------------
if __name__ == "__main__":
    app = MoodMusicApp()
    app.mainloop()
