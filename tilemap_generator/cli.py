import matplotlib.pyplot as plt
import matplotlib.image as mimg
import numpy as np
from datetime import datetime
from os import getcwd
from sys import argv as args
from sys import stdout
from pathlib import Path


def log(message: str, endline: bool = False):
    now: datetime = datetime.now()
    now_str: str = now.strftime("%Y-%m-%d %H:%M:%S")
    if not endline:
        print(f"{now_str} [\u001b[32mtilemap-generator\u001b[0m] {message}")
        return
    print(f"{now_str} [\u001b[32mtilemap-generator\u001b[0m] {message}", end="\r")


def crop(image: np.ndarray, tile_size: tuple) -> np.ndarray:
    im_h, im_w, ch = image.shape
    tile_h, tile_w = tile_size[0], tile_size[1]
    tiled = image.reshape(im_h // tile_h, tile_h, im_w // tile_w, tile_w, ch)
    tiled = tiled.swapaxes(1, 2)
    return tiled.reshape(-1, 16, 16, 3)


def generate(outDir: Path, tiles: np.ndarray):
    tile_map = np.zeros(tiles.shape[0], dtype=">H")
    tile_index = 0
    for i, tile in enumerate(tiles[:-1]):
        log(f"Finding Unique - {i+1}/{tiles.shape[0]}", True)
        found = False
        if tile_map[i] != tile_index:
            continue
        for j, compare in enumerate(tiles[i + 1 :]):
            j += i + 1
            if tile_map[j] == tile_index and np.any(tile != compare):
                tile_map[j] += 1
                found = True
        if found:
            tile_index += 1
    log(f"Finding Unique {tiles.shape[0]}/{tiles.shape[0]}")
    log(f"Total Unique {tile_index+1}")
    for i in range(tile_index + 1):
        log(f"Saving Tile - {i+1}/{tile_index+1}", True)
        mimg.imsave(
            outDir.joinpath("tiles").joinpath(f"{i}.bmp"),
            tiles[np.argmax(tile_map == i)],
        )
    log(f"Saving Tile - {tile_index+1}/{tile_index+1}")
    log("Generating level.dat")
    with open(outDir.joinpath("level.dat"), "wb") as file:
        file.write(tile_map.tobytes())


def start(path: Path):
    image: np.ndarray = mimg.imread(path)
    log("Cropping Image")
    tiles = crop(image, (16, 16))
    out = Path(getcwd()).joinpath("out")
    out.mkdir(parents=True, exist_ok=True)
    out.joinpath("tiles").mkdir(parents=True, exist_ok=True)
    generate(out, tiles)
    log("Done")


def main():
    if len(args) != 2:
        print("[\u001b[31merror\u001b[0m] FATAL Invalid Argument")
        raise ValueError()
    location: Path = Path(getcwd()).joinpath(args[1])
    start(location)
