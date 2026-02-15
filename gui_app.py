import customtkinter as ctk
from PIL import Image
import os
import json
from datetime import datetime
from music_player import get_song_for_mood, play_song

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MoodMusicApp(ctk.CTk):
    def __init__(self, mood: str):
        super().__init__()

        self.mood = mood

        self.title("Mood-Based Music Player")
        self.geometry("420x520")
        self.resizable(False, False)

        # ---------------- Title ----------------
        title = ctk.CTkLabel(
            self,
            text="🎧 Mood-Based Music Player",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=20)

        # ---------------- Mood Label ----------------
        mood_label = ctk.CTkLabel(
            self,
            text=f"Predicted Mood: {self.mood}",
            font=("Segoe UI", 16)
        )
        mood_label.pack(pady=10)

        # ---------------- Mood Image ----------------
        self.load_mood_image()

        # ---------------- Feedback Section ----------------
        feedback_label = ctk.CTkLabel(
            self,
            text="Did this song match your mood?",
            font=("Segoe UI", 14)
        )
        feedback_label.pack(pady=20)

        feedback_frame = ctk.CTkFrame(self)
        feedback_frame.pack(pady=10)

        yes_btn = ctk.CTkButton(
            feedback_frame,
            text="👍 Yes",
            width=120,
            command=lambda: self.save_feedback(True)
        )
        yes_btn.grid(row=0, column=0, padx=10)

        no_btn = ctk.CTkButton(
            feedback_frame,
            text="👎 No",
            width=120,
            command=lambda: self.save_feedback(False)
        )
        no_btn.grid(row=0, column=1, padx=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=15)

    # ---------------- Load Image Safely ----------------
    def load_mood_image(self):
        img_path = os.path.join("images", f"{self.mood}.png")

        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = ctk.CTkImage(light_image=img, size=(200, 200))
            img_label = ctk.CTkLabel(self, image=img, text="")
            img_label.image = img
            img_label.pack(pady=10)
        else:
            fallback = ctk.CTkLabel(
                self,
                text="(No image found)",
                font=("Segoe UI", 12)
            )
            fallback.pack(pady=10)

    # ---------------- Feedback Storage ----------------
    def save_feedback(self, is_correct: bool):
        feedback = {
            "mood": self.mood,
            "correct": is_correct,
            "timestamp": datetime.now().isoformat()
        }

        os.makedirs("feedback", exist_ok=True)
        file_path = os.path.join("feedback", "feedback.json")

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(feedback)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        self.status_label.configure(
            text="✅ Feedback saved. Thank you!"
        )

    def play_music(self):
        song_path, song_name = get_song_for_mood(self.mood)

        if song_path:
            play_song(song_path)
        else:
            self.status_label.configure(
                text="❌ No song found for this mood"
            )


def launch_gui(mood: str):
    app = MoodMusicApp(mood)
    app.mainloop()


if __name__ == "__main__":
    TEST_MOOD = "Relaxed"   # change this to test other moods
    app = MoodMusicApp(TEST_MOOD)
    app.mainloop()
