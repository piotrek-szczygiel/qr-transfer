import io
import math
from threading import Thread

import cv2
import numpy as np
import segno
from tqdm import trange

# https://www.qrcode.com/en/about/version.html
# Medium error correction
QR_SIZE = {
    5: 84,
    6: 106,
    7: 122,
    8: 152,
    9: 180,
    10: 213,
    11: 251,
    12: 287,
    13: 331,
    14: 362,
    15: 412,
}


def encode_frame(a, b, c, version=15, qr_size=400):
    data = []
    for x in (a, b, c):
        if x is not None:
            data.append(
                segno.make(
                    x, error="M", version=version, mode="byte", boost_error=False
                )
            )
        else:
            data.append(None)

    size = len(data[0].matrix)
    rgb = np.zeros((size, size, 3), np.uint8)

    for i in range(3):
        if data[i] is not None:
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

    print(f"File size: {size}B")
    frames = []
    for i in trange(0, len(chunks), 3, desc="encoding", unit="codes"):
        a = chunks[i] if i < len(chunks) else None
        b = chunks[i + 1] if i + 1 < len(chunks) else None
        c = chunks[i + 2] if i + 2 < len(chunks) else None
        frames.append(encode_frame(a, b, c, version=version, qr_size=qr_size))

    return frames
