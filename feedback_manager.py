import csv
import os
from datetime import datetime

FILE_NAME = "feedback.csv"

def save_feedback(mood, song, liked):
    file_exists = os.path.exists(FILE_NAME)

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["mood", "song", "liked", "time"])
        writer.writerow([mood, song, liked, datetime.now()])


def get_song_scores(mood):
    scores = {}

    if not os.path.exists(FILE_NAME):
        return scores

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["mood"] == mood:
                song = row["song"]
                liked = int(row["liked"])
                scores[song] = scores.get(song, 0) + (1 if liked else -1)

    return scores
