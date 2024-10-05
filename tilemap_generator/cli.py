import matplotlib.image as mimg
import numpy as np
from datetime import datetime
from os import getcwd
from sys import argv as args
from pathlib import Path


def log(message: str, endline: bool = False):
    now: datetime = datetime.now()
    now_str: str = now.strftime("%Y-%m-%d %H:%M:%S")
    if not endline:
        print(f"{now_str} [\u001b[32mapplication\u001b[0m] {message}")
        return
    print(f"{now_str} [\u001b[32mapplication\u001b[0m] {message}", end="\r")


def start(path: Path):
    image: np.ndarray = mimg.imread(path)
    im_h, im_w, ch = image.shape
    tile_h, tile_w = (16, 16)
    log("Cropping Image")
    tiled = image.reshape(im_h // tile_h, tile_h, im_w // tile_w, tile_w, ch)
    tiled = tiled.swapaxes(1, 2)
    new = tiled.reshape(-1, 16, 16, 3)
    log("Generating Tilemap")
    out = Path(getcwd()).joinpath("out")
    out.mkdir(parents=True, exist_ok=True)
    for i, tile in enumerate(new):
        mimg.imsave(out.joinpath(f"{i}.bmp"), tile)


def main():
    if len(args) != 2:
        print("[\u001b[31merror\u001b[0m] FATAL Invalid Argument")
        raise ValueError()
    location: Path = Path(getcwd()).joinpath(args[1])
    start(location)
