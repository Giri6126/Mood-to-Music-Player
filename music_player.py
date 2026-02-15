import pygame
import os
import random

pygame.mixer.init()

BASE_PATH = os.path.join(os.getcwd(), "music")

MOOD_STRATEGY = {
    "Happy": ["Happy"],
    "Sad": ["Sad", "Motivation"],
    "Angry": ["Happy", "Relaxed"],
    "Neutral": ["Happy", "Motivation", "Relaxed"],
    "Relaxed": ["Relaxed"]
}

def get_song_for_mood(mood):
    playlists = MOOD_STRATEGY.get(mood, [])
    songs = []

    for playlist in playlists:
        folder = os.path.join(BASE_PATH, playlist)
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if f.endswith(".mp3"):
                    songs.append(os.path.join(folder, f))

    if not songs:
        return None, None

    song = random.choice(songs)
    return song, os.path.basename(song)

def play_song(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def stop_song():
    pygame.mixer.music.stop()
