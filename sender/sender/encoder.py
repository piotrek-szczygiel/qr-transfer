import io
import math

import numpy as np
import segno
from kivy.core.image import Image as CoreImage
from PIL import Image


def encode_frame(a, b, c, frame_size):
    assert len(a) == len(b) == len(c)

    data = [segno.make(x) for x in (a, b, c)]
    size = len(data[0].matrix)

    rgb = np.zeros((size, size, 3), "uint8")
    for i in range(3):
        rgb[..., i] = np.array(data[i].matrix) * 255

    scale = math.ceil(frame_size / size)
    img = Image.fromarray(rgb).resize((size * scale, size * scale))

    buffer = io.BytesIO()
    img.save(buffer, format="png")
    buffer.seek(0)
    return CoreImage(io.BytesIO(buffer.read()), ext="png").texture


def generate_frames(data, frame_size=400):
    return [encode_frame(*data[i : i + 3], frame_size) for i in range(0, len(data), 3)]
