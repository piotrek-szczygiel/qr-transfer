import uuid

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from .encoder import generate_frames


class Ui(BoxLayout):
    def __init__(self, **kwargs):
        super(Ui, self).__init__(**kwargs)

        self.frames = generate_frames([str(uuid.uuid4()) for _ in range(99)])
        self.cursor = 0

        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        self.ids.frame_a.texture = self.frames[self.cursor]
        self.ids.frame_b.texture = self.frames[self.cursor]
        self.ids.frame_c.texture = self.frames[self.cursor]
        self.ids.frame_d.texture = self.frames[self.cursor]
        self.cursor = (self.cursor + 1) % len(self.frames)


class SenderApp(App):
    from kivy.config import Config

    Config.set("graphics", "width", 800)
    Config.set("graphics", "height", 800)
    Config.set("modules", "monitor", "")

    def build(self):
        return Ui()


def run():
    SenderApp().run()
