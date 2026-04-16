import random

QUOTES = {

    "Happy": [
        "Happiness is not something ready made. It comes from your own actions.",
        "Let your smile change the world, but never let the world change your smile.",
        "The best way to pay for a lovely moment is to enjoy it.",
        "Joy is contagious. Spread it everywhere you go.",
        "Do more of what makes your soul shine."
    ],

    "Sad": [
        "Tough times never last, but tough people do.",
        "Every storm runs out of rain.",
        "Sometimes when you're in a dark place, you think you've been buried, but actually you've been planted.",
        "Your current situation is not your final destination.",
        "Healing takes time — and that's okay."
    ],

    "Angry": [
        "For every minute you remain angry, you give up sixty seconds of peace.",
        "Speak when you are angry and you will make the best speech you will ever regret.",
        "Calm mind brings inner strength and self-confidence.",
        "Anger doesn't solve anything. It builds nothing.",
        "Peace begins with a deep breath."
    ],

    "Neutral": [
        "Small steps today lead to big results tomorrow.",
        "Consistency beats intensity.",
        "Progress is progress, no matter how small.",
        "Every day is a chance to grow.",
        "Stay curious. Stay learning."
    ],

    "Relaxed": [
        "Almost everything will work again if you unplug it for a few minutes — including you.",
        "Sometimes the most productive thing you can do is relax.",
        "Breathe in calm, breathe out stress.",
        "Slow down. You're doing just fine.",
        "Peace comes from within."
    ]
}


def get_quote_for_mood(mood):
    quotes = QUOTES.get(mood, ["Enjoy the music and relax."])
    return random.choice(quotes)