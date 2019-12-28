import io
import math
from threading import Thread

import cv2
import numpy as np
import segno
from tqdm import trange

# https://www.qrcode.com/en/about/version.html
QR_SIZE = {
    1: 17,
    2: 32,
    3: 53,
    4: 78,
    5: 106,
    6: 134,
    7: 154,
    8: 192,
    9: 230,
    10: 271,
    11: 321,
    12: 367,
    13: 425,
    14: 458,
    15: 520,
    16: 586,
    17: 644,
    18: 718,
    19: 792,
    20: 858,
}


def encode_frame(a, b, c, version=15, qr_size=400):
    data = [
        segno.make(x, error="L", version=version, mode="byte", boost_error=False)
        for x in (a, b, c)
    ]

    size = len(data[0].matrix)
    rgb = np.zeros((size, size, 3), np.uint8)

    for i in range(3):
        rgb[..., i] = (1 - np.array(data[i].matrix)) * 255

    scale = qr_size // size

    scaled = cv2.resize(
        rgb, (size * scale, size * scale), interpolation=cv2.INTER_NEAREST
    )
    return scaled


def generate_frames(data, version, qr_size):
    size = len(data)
    chunk_size = QR_SIZE[version]
    chunks = []

    for i in range(0, size, chunk_size):
        chunks.append(data[i : i + chunk_size])

    if len(chunks) % 12 != 0:
        for _ in range(12 - len(chunks) % 12):
            chunks.append("")

    triplets = []
    for i in range(0, len(chunks), 3):
        triplets.append((chunks[i], chunks[i + 1], chunks[i + 2]))

    print(f"File size: {size}B")
    frames = []
    for i in trange(len(triplets), desc="encoding", unit="codes"):
        frames.append(encode_frame(*triplets[i], version=version, qr_size=qr_size))

    return frames
