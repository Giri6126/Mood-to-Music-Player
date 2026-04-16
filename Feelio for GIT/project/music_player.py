import pygame
import os
import random

pygame.mixer.init()

# Create event when song ends
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "static", "music")

MOOD_STRATEGY = {
    "Happy": ["Happy"],
    "Sad": ["Sad", "Motivation"],
    "Angry": ["Happy", "Relaxed"],
    "Neutral": ["Happy", "Motivation", "Relaxed"],
    "Relaxed": ["Relaxed"]
}

current_song = None

def get_song_for_mood(mood):
    print("Mood received:", mood)

    playlists = MOOD_STRATEGY.get(mood, ["Happy"])
    print("Playlists:", playlists)

    all_songs = []

    for p in playlists:
        folder = os.path.join(BASE_PATH, p)
        print("Checking folder:", folder)

        if os.path.exists(folder):
            songs = [
                s for s in os.listdir(folder)
                if s.endswith(".mp3")
            ]
            print("Songs found:", songs)

            all_songs.extend([(p, s) for s in songs])
        else:
            print("Folder NOT found:", folder)

    if not all_songs:
        print("No songs found!")
        return None, None

    import random
    mood_folder, song = random.choice(all_songs)

    print("Selected:", song)

    return f"static/music/{mood_folder}/{song}", song

def play_song(path):
    global current_song
    current_song = path
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()


def pause_song():
    pygame.mixer.music.pause()


def resume_song():
    pygame.mixer.music.unpause()


def stop_song():
    pygame.mixer.music.stop()