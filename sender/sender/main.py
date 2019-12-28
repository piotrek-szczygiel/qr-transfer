import argparse
import pickle
import sys
from pathlib import Path

from .app import App
from .encoder import generate_frames


def run():
    parser = argparse.ArgumentParser(description="Send data through photons.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-l", "--load", action="store", dest="filename", help="file to load"
    )
    group.add_argument(
        "-c", "--cache", action="store_true", dest="cache", help="use cached data"
    )
    parser.add_argument(
        "-f",
        "--freq",
        action="store",
        dest="frequency",
        type=int,
        default=4,
        help="frequency",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store",
        dest="version",
        type=int,
        choices=range(1, 21),
        default=15,
        help="qr code version",
    )
    parser.add_argument(
        "-s",
        "--save",
        action="store",
        dest="qr_size",
        type=int,
        default=400,
        help="maximum single qr size in pixels",
    )
    args = parser.parse_args()

    cache_filename = Path.home().joinpath(".qr.cache")

    if args.filename:
        try:
            with open(args.filename, "rb") as file:
                data = file.read()
                frames = generate_frames(data, args.version, args.qr_size)
        except FileNotFoundError:
            print(f"unable to open file {args.filename}")
            sys.exit(1)

        print(f"saving frames to cache file {cache_filename}")
        with open(cache_filename, "wb") as cache:
            pickle.dump(frames, cache)
    elif args.cache:
        try:
            with open(cache_filename, "rb") as cache:
                frames = pickle.load(cache)
        except FileNotFoundError:
            print(f"cache file {cache_filename} does not exist")
            sys.exit(1)

    App(frames, frequency=args.frequency).run()


if __name__ == "__main__":
    run()
