from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.config import Config
import uuid
import qrcode
import io

Config.set("modules", "monitor", "")


class MyApp(App):
    def build(self):
        self.title = "QR Sender"

        self.display = True
        self.data = [uuid.uuid4() for _ in range(100)]
        self.cursor = 0

        self.buffer = io.BytesIO()
        self.image = Image(source="")

        layout = BoxLayout()
        layout.add_widget(self.image)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

        return layout

    def update(self, dt):
        self.buffer.truncate(0)
        self.buffer.seek(0)

        qr = qrcode.make(self.data[self.cursor])
        qr.save(self.buffer, ext="png")

        self.cursor = (self.cursor + 1) % len(self.data)

        self.buffer.seek(0)
        image = io.BytesIO(self.buffer.read())
        self.image.texture = CoreImage(image, ext="png").texture


def run():
    MyApp().run()
