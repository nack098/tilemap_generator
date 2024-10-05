import matplotlib as plt
import numpy as np
from os import getcwd
from sys import argv as args
from pathlib import Path


def start(path: Path):
    raise NotImplementedError()


def main():
    if len(args) != 2:
        print("[\u001b[31merror\u001b[0m] FATAL Invalid Argument")
        raise ValueError()
    location: Path = Path(getcwd()).joinpath(args[1])
    start(location)
