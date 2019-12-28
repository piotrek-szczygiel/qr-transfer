import io
import math
from threading import Thread

import cv2
import numpy as np
import segno
from tqdm import trange

QR_VERSION = 20
MAX_CHUNK_SIZE = 858


def encode_frame(a, b, c, scale=2):
    data = [
        segno.make(x, error="L", version=QR_VERSION, mode="byte", boost_error=False)
        for x in (a, b, c)
    ]

    size = len(data[0].matrix)
    rgb = np.zeros((size, size, 3), np.uint8)

    for i in range(3):
        rgb[..., i] = (1 - np.array(data[i].matrix)) * 255

    scaled = cv2.resize(rgb, (size * 4, size * 4), interpolation=cv2.INTER_NEAREST)
    return scaled


def generate_frames(data):
    size = len(data)
    chunk_size = MAX_CHUNK_SIZE
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
        frames.append(encode_frame(*triplets[i]))

    return frames
