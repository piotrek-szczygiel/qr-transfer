import os
import uuid

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from .encoder import generate_frames


class Ui(BoxLayout):
    def __init__(self, **kwargs):
        super(Ui, self).__init__(**kwargs)
        self.clock = None

    def update(self, dt):
        self.ids.frame_a.texture = self.frames[self.cursor]
        self.ids.frame_b.texture = self.frames[self.cursor]
        self.ids.frame_c.texture = self.frames[self.cursor]
        self.ids.frame_d.texture = self.frames[self.cursor]
        self.cursor = (self.cursor + 1) % len(self.frames)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        if self.clock:
            self.clock.cancel()

        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0]), "rb") as stream:
            self.frames = generate_frames(stream.read())
            self.cursor = 0
            self.ids.start.disabled = False
        self.dismiss_popup()

    def start(self):
        self.clock = Clock.schedule_interval(self.update, 1.0 / 30.0)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SenderApp(App):
    from kivy.config import Config

    Config.set("graphics", "width", 730)
    Config.set("graphics", "height", 800)
    Config.set("modules", "monitor", "")

    def build(self):
        from kivy.core.window import Window

        Window.clearcolor = (1, 1, 1, 1)
        return Ui()


def run():
    SenderApp().run()
