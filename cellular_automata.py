from __future__ import annotations
import pygame

import numpy as np
from typing import List
from dataclasses import dataclass
from scipy.ndimage import generic_filter
import matplotlib.pyplot as plt
from abc import ABC
from main import Viewer


class Neighborhood(ABC):
    key: int
    N: int
    binary_form: np.array

    def __init__(self, N: int, key: int):
        self.N = N
        assert 0 <= key < 2 ** N, f"key should be in range (0..512), but is {key}"
        self.key = key
        self.binary_form = np.array([int(char)
                                     for char in bin(key)[2:].rjust(N, "0")])

    @property
    def core(self):
        return self.binary_form[self.N//2]

    @classmethod
    def from_binary_form(cls, binary_form: np.array):
        return cls(key=cls._key(binary_form))

    @staticmethod
    def _key(binary_form: np.array):
        return binary_form.dot(2 ** np.arange(binary_form.size)[::-1])

    def __str__(self) -> str:
        return str(self.binary_form)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return np.all(self.binary_form == other.binary_form)


class CubicNeighborhood(Neighborhood):
    def __init__(self, key: int):
        Neighborhood.__init__(self, 9, key)


class HexNeighborhood(Neighborhood):
    def __init__(self, key: int):
        Neighborhood.__init__(self, 7, key)


class TriNeighborhood(Neighborhood):
    def __init__(self, key: int):
        Neighborhood.__init__(self, 4, key)


@dataclass
class CubicBoard:
    binary_matrix: np.array

    def stencil_form(self, mode: str = "constant") -> np.array:
        def _mapping_function(mat):
            return CubicNeighborhood.from_binary_form(mat.flatten().astype(int)).key

        return generic_filter(
            self.binary_matrix, _mapping_function, (3, 3), mode=mode, cval=0, output="int"
        )

    @classmethod
    def from_stencils(self, stencil_form: np.array) -> CubicBoard:
        return CubicBoard((stencil_form >> 4) % 2)

    @classmethod
    def random(self, N: int, seed: int = None, fill_rate: float = 0.5):
        if seed is not None:
            np.random.seed(seed)

        return CubicBoard(np.random.rand(N, N) < fill_rate)

    def __repr__(self):
        return str(1 * self.binary_matrix)

    def plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
        return plt.spy(self.binary_matrix, origin="upper")

    def __eq__(self, other: CubicBoard):
        return np.all(self.binary_matrix == other.binary_matrix)

##########


def original_rules():
    mapping = np.zeros(512, dtype=int)

    for key in range(512):
        stencil = CubicNeighborhood(key)
        if stencil.core == 0:
            mapping[key] = (np.sum(stencil.binary_form) == 3)
        else:
            mapping[key] = 1 < (np.sum(stencil.binary_form) - 1) < 4

    return mapping


def update_board(board: CubicBoard, mapping: List[int]) -> CubicBoard:

    stencil_form = board.stencil_form('wrap')

    def _mapping_function(key):
        return mapping[int(key)]

    new_binary_form = generic_filter(stencil_form, _mapping_function, 1,)
    return CubicBoard(new_binary_form)


if __name__ == "__main__":
    resolution = (1000, 1000)
    N = 100
    mapping = original_rules()

    def init():
        return CubicBoard.random(N, fill_rate=0.5).binary_matrix

    def update(binary_matrix):
        return update_board(CubicBoard(binary_matrix), mapping).binary_matrix

    viewer = Viewer(resolution, init, update)
    viewer.run()
