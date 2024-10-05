import matplotlib.image as mimg
import numpy as np
from os import getcwd
from sys import argv as args
from pathlib import Path


def start(path: Path):
    image: np.ndarray = mimg.imread(path)
    im_h, im_w, ch = image.shape
    tile_h, tile_w = (16, 16)
    print("[\u001b[32mapplication\u001b[0m] Cropping Image...")
    tiled = image.reshape(im_h // tile_h, tile_h, im_w // tile_w, tile_w, ch)
    tiled = tiled.swapaxes(1, 2)
    new = tiled.reshape(-1, 16, 16, 3)
    print("[\u001b[32mapplication\u001b[0m] Generating Tilemap")
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
