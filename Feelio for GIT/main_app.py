import threading
import random
import customtkinter as ctk
from PIL import Image
import pygame
pygame.mixer.init()
from project.music_player import SONG_END
import os, json
from datetime import datetime
from project.quotes import get_quote_for_mood
from project.model_utils import predict_mood_from_answers
from project.music_player import (
    get_song_for_mood,
    play_song,
    pause_song,
    resume_song,
    stop_song
)
# ---------------- Mood Color Themes ----------------

MOOD_THEMES = {
    "Happy": {
        "bg": "#FFD54F",
        "accent": "#FFA000"
    },
    "Sad": {
        "bg": "#5C6BC0",
        "accent": "#3949AB"
    },
    "Angry": {
        "bg": "#EF5350",
        "accent": "#C62828"
    },
    "Neutral": {
        "bg": "#78909C",
        "accent": "#546E7A"
    },
    "Relaxed": {
        "bg": "#80CBC4",
        "accent": "#26A69A"
    }
}
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

import pygame


class MoodMusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mood to Music Player")
        self.geometry("450x700")
        self.resizable(False, False)

        self.inputs = {}
        self.song_path = None
        self.current_mood = None

        self.build_questionnaire()
        #self.check_song_end()

    # ---------------- Questionnaire ----------------
    def build_questionnaire(self):

        ctk.CTkLabel(
            self,
            text="🎵 Mood Based Music Player",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=20)

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

        ctk.CTkLabel(
            frame,
            text=text,
            width=260,
            anchor="w"
        ).pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=80)
        entry.pack(side="right", padx=10)

        return entry

    # ---------------- Mood Prediction ----------------
    def predict_and_play(self):
        stop_song()
        try:
            values = [float(self.inputs[k].get()) for k in self.inputs]
        except:
         return

    # Run prediction in background thread
        threading.Thread(
            target=self.predict_mood_thread,
            args=(values,),
            daemon=True
        ).start()


    # ---------------- Result Screen ----------------
    def load_result_screen(self, mood):
        for widget in self.winfo_children():
            widget.destroy()
        # Apply mood theme
        theme = MOOD_THEMES.get(mood, None)

        if theme:
            self.configure(fg_color=theme["bg"])

        ctk.CTkLabel(
            self,
            text=f"Mood based music player",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(20,10))

        mood_card = ctk.CTkFrame(self, corner_radius=20)
        mood_card.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(
            mood_card,
            text=f"Predicted Mood: {mood}",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        # Mood Image
        img_path = f"images/{mood}.png"

        if os.path.exists(img_path):
            img = Image.open(img_path).resize((220,220))
            img = ctk.CTkImage(light_image=img, size=(220, 220))

            label = ctk.CTkLabel(self, image=img, text="")
            label.image = img
            label.pack(pady=10)
        # Mood Quote
        quote = get_quote_for_mood(mood)

        quote_frame = ctk.CTkFrame(
             self,
             corner_radius=15
        )

        quote_frame.pack(pady=20, padx=25, fill="x")

        ctk.CTkLabel(
            quote_frame,
            text=f"💬 {quote}",
            wraplength=360,
            justify="center",
            font=("Segoe UI", 15, "italic")
        ).pack(pady=18, padx=15)

        # Get song
        song_path, song_name = get_song_for_mood(mood)

        if song_path:
            self.song_path = song_path

            self.now_playing_label = ctk.CTkLabel(
                self,
                text=f"🎶 Now Playing: {song_name}"
            )
            self.now_playing_label.pack(pady=10)

            # Start music after UI loads
            self.after(300, lambda: play_song(self.song_path))

       # ---------- Music Visualizer ----------
        self.visualizer_frame = ctk.CTkFrame(self, height=100, corner_radius=15)
        self.visualizer_frame.pack(pady=15, padx=30, fill="x")

       # Prevent frame resizing
        self.visualizer_frame.pack_propagate(False)

        bars_container = ctk.CTkFrame(self.visualizer_frame, fg_color="transparent")
        bars_container.pack(expand=True)

        self.bars = []

        theme = MOOD_THEMES.get(self.current_mood, {})
        bar_color = theme.get("accent", "#1f6aa5")

        for i in range(16):
             bar = ctk.CTkFrame(
                  bars_container,
                  width=8,
                  height=20,
                  corner_radius=4,
                  fg_color=bar_color
            )

             bar.grid(row=0, column=i, padx=3)
             self.bars.append(bar)

        self.animate_visualizer()


        # Player Controls
        self.build_player_controls()

        # Feedback
        self.feedback_buttons(mood)
        self.monitor_song()
    # ---------------- Player Controls ----------------
    def build_player_controls(self):

        controls = ctk.CTkFrame(self, corner_radius=25)
        controls.pack(pady=20, padx=40)

        play_btn = ctk.CTkButton(
            controls,
            text="▶",
            height=40,
            corner_radius=20,
            width=80,
            hover_color="#2ecc71",
            command=lambda: play_song(self.song_path)
        )
        play_btn.grid(row=0, column=0, padx=5)

        pause_btn = ctk.CTkButton(
            controls,
            text="⏸ Pause",
            height=40,
            corner_radius=20,
            width=80,
            hover_color="#2ecc71",
            command=pause_song
        )
        pause_btn.grid(row=0, column=1, padx=5)

        resume_btn = ctk.CTkButton(
            controls,
            text="▶ Resume",
            height=40,
            corner_radius=20,
            width=80,
            hover_color="#2ecc71",
            command=resume_song
        )
        resume_btn.grid(row=0, column=2, padx=5)

        stop_btn = ctk.CTkButton(
            controls,
            text="⏹ Stop",
            height=40,
            corner_radius=20,
            width=80,
            hover_color="#2ecc71",
            command=stop_song
        )
        stop_btn.grid(row=0, column=3, padx=5)

        next_btn = ctk.CTkButton(
            controls,
            text="⏭ Next",
            height=40,
            corner_radius=20,
            width=80,
            hover_color="#2ecc71",
            command=self.play_next_song
        )
        next_btn.grid(row=1, column=1, columnspan=2, pady=10)

    # ---------------- Next Song ----------------
    def play_next_song(self):

        if not self.current_mood:
            return

        song_path, song_name = get_song_for_mood(self.current_mood)

        if song_path:
            self.song_path = song_path
            play_song(song_path)

            self.now_playing_label.configure(
                text=f"🎶 Now Playing: {song_name}"
            )

    # ---------------- Feedback ----------------
    def feedback_buttons(self, mood):

        frame = ctk.CTkFrame(self)
        frame.pack(pady=20)

        ctk.CTkLabel(
            frame,
            text="Did this song match your mood?"
        ).grid(row=0, column=0, columnspan=2, pady=5)

        ctk.CTkButton(
            frame,
            text="👍 Yes",
            command=lambda: self.save_feedback(mood, True)
        ).grid(row=1, column=0, padx=10)

        ctk.CTkButton(
            frame,
            text="👎 No",
            command=lambda: self.save_feedback(mood, False)
        ).grid(row=1, column=1, padx=10)

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

        ctk.CTkLabel(
            self,
            text="✅ Feedback saved. Thank you!"
        ).pack(pady=10)

    def monitor_song(self):
        if not pygame.mixer.music.get_busy() and self.song_path:
            self.play_next_song()

        self.after(3000, self.monitor_song)

    

    def animate_visualizer(self):
        if hasattr(self, "bars"):
            for bar in self.bars:
                height = random.randint(10, 80)
                bar.configure(height=height)
        self.after(200, self.animate_visualizer)


    def predict_mood_thread(self, values):
        mood = predict_mood_from_answers(*values)
        self.current_mood = mood

    # Update GUI safely in main thread
        self.after(0, lambda: self.load_result_screen(mood))

# ---------------- Run App ----------------
if __name__ == "__main__":
    app = MoodMusicApp()
    app.mainloop()