from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.config import Config
import segno
import io
import numpy as np
import uuid
from PIL import Image as PilImage

Config.set("modules", "monitor", "")


def generate_frame(a, b, c, scale=1):
    assert len(a) == len(b) == len(c)

    data = [segno.make(x) for x in (a, b, c)]
    size = len(data[0].matrix)

    rgb = np.zeros((size, size, 3), "uint8")
    for i in range(3):
        rgb[..., i] = np.array(data[i].matrix) * 255

    img = PilImage.fromarray(rgb).resize((size * scale, size * scale))
    buffer = io.BytesIO()
    img.save(buffer, format="png")
    buffer.seek(0)
    return CoreImage(io.BytesIO(buffer.read()), ext="png").texture


def frames(data):
    frames = []
    for i in range(0, len(data), 3):
        frames.append(generate_frame(*data[i : i + 3], scale=10))
    return frames


class QrSender(App):
    def build(self):
        self.title = "QR Sender"
        self.image = Image()

        self.frames = frames([str(uuid.uuid4()) for _ in range(99)])
        self.cursor = 0

        layout = BoxLayout()
        layout.add_widget(self.image)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return layout

    def update(self, dt):
        self.image.texture = self.frames[self.cursor]
        self.cursor = (self.cursor + 1) % len(self.frames)


def run():
    QrSender().run()
