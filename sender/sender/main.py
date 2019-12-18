from .app import App
from .encoder import generate_frames


def run():
    with open("poetry.lock", "rb") as file:
        data = file.read()

    App(generate_frames(data)).run()
