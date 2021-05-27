import numpy as np
import pygame
from time import sleep, time
from main import Viewer


def n_neighbors(A):
    count = np.zeros_like(A, dtype=int)

    count[:, :-1] += A[:, 1:]  # right
    count[:, 1:] += A[:, :-1]  # left
    count[:-1, :] += A[1:, :]  # up
    count[1:, :] += A[:-1, :]  # down

    count[:-1, :-1] += A[1:, 1:]  # up-right
    count[1:, 1:] += A[:-1, :-1]  # down-left
    count[:-1, 1:] += A[1:, :-1]  # up-left
    count[1:, :-1] += A[:-1, 1:]  # down-right

    return count


def rules(A):
    """
    1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    """
    count = n_neighbors(A)

    # | (np.random.rand(N,N) < 0.04)
    return ((A & ((count == 2) | (count == 3))) | ((count == 3) & (~A)))


if __name__ == "__main__":
    resolution = (1000, 1000)
    N = 1000

    def init():
        board = np.random.rand(N, N) < 0.5
        
        M = 50
        m = 0.7
        k = int(m*(N/M))

        for i in range(M):
            b = i*N//M
            board[b:b + k, :] = 0
            board[:, b:b + k] = 0

        return board


    viewer = Viewer(resolution, init, rules)
    viewer.run()

