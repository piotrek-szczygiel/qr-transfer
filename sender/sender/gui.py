import uuid

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from .encoder import generate_frames

Config.set("modules", "monitor", "")


class Gui(App):
    def build(self):
        self.title = "QR Sender"
        self.image = Image()

        self.frames = generate_frames([str(uuid.uuid4()) for _ in range(99)])
        self.cursor = 0

        layout = BoxLayout()
        layout.add_widget(self.image)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return layout

    def update(self, dt):
        self.image.texture = self.frames[self.cursor]
        self.cursor = (self.cursor + 1) % len(self.frames)
