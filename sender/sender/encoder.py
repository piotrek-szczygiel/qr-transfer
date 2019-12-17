import io
import math
from threading import Thread

import numpy as np
import segno
from kivy.core.image import Image as CoreImage
from PIL import Image

# Maximum data size a QR Code, version 40, with minimal error correction can hold
QR_VERSION = 20
MAX_CHUNK_SIZE = 858


def encode_frame(a, b, c):
    data = [
        segno.make(x, error="L", version=QR_VERSION, mode="byte", boost_error=False)
        for x in (a, b, c)
    ]
    size = len(data[0].matrix)

    rgb = np.zeros((size, size, 3), "uint8")
    for i in range(3):
        rgb[..., i] = np.array(data[i].matrix) * 255

    img = Image.fromarray(rgb)

    scale = math.ceil(400 / size)
    img = img.resize((size * scale, size * scale))

    buffer = io.BytesIO()
    img.save(buffer, format="png")
    buffer.seek(0)
    return CoreImage(io.BytesIO(buffer.read()), ext="png").texture


def generate_frames(data):
    size = len(data)
    chunk_size = MAX_CHUNK_SIZE
    chunks = []

    for i in range(0, size, chunk_size):
        chunks.append(data[i : i + chunk_size])

    if len(chunks) % 3 != 0:
        for _ in range(3 - len(chunks) % 3):
            chunks.append("")

    triplets = []
    for i in range(0, len(chunks), 3):
        triplets.append((chunks[i], chunks[i + 1], chunks[i + 2]))

    print(f"File size: {size}B")
    print(f"Triplets: {len(triplets)}")

    frames = []
    for i, t in enumerate(triplets):
        print(f"Encoding triplet {i}/{len(triplets)}...")
        frames.append(encode_frame(*t))

    return frames
