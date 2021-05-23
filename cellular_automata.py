from __future__ import annotations

import numpy as np
from typing import List
from dataclasses import dataclass
from scipy.ndimage import generic_filter
import matplotlib.pyplot as plt


class CubicStencil:
    def __init__(self, key: int):
        assert 0 <= key < 512, f"key should be in range (0..512), but is {key}"

        self.key = key
        binary_form = [int(char) for char in bin(key)[2:].rjust(9, "0")]
        self.mat = np.reshape(binary_form, (3, 3))

    @classmethod
    def from_mat(self, mat: np.array):
        key = CubicStencil._key(mat)
        return CubicStencil(key)

    @property
    def core(self):
        return self.mat[1, 1]

    def _key(mat: np.array) -> int:
        b = mat.flatten()
        return b.dot(2 ** np.arange(b.size)[::-1])

    def __repr__(self) -> str:
        return str(self.mat)


@dataclass
class CubicBoard:
    binary_form: np.array

    def stencil_form(self, mode: str = "constant") -> np.array:
        def _mapping_function(mat_stencil):
            return CubicStencil.from_mat(np.reshape(mat_stencil.astype(int), (3, 3))).key

        return generic_filter(
            self.binary_form, _mapping_function, (3, 3), mode=mode, cval=0, output="int"
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
        return str(1 * self.binary_form)

    def plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
        return plt.spy(self.binary_form, origin="upper")

    def __eq__(self, other: CubicBoard):
        return np.all(self.binary_form == other.binary_form)
