import pygame
from time import time, sleep
import numpy as np


class Viewer:
    def __init__(self, resolution, automata_init, automata_update, max_fps: int = -1):
        # Import and initialize the pygame library

        self.resolution = resolution

        self.automata_init = automata_init
        self.automata_update = automata_update
        self.max_fps = max_fps

        self.frametime = 0

    def run(self):
        pygame.init()

        # Set up the drawing window
        self.screen = pygame.display.set_mode(self.resolution)

        board = self.automata_init()

        running = True

        tic = time()

        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the background with white
            self.screen.fill((255, 255, 255))

            im = np.tile(board, [3, 1, 1]).T * 255
            surface = pygame.surfarray.make_surface(im)
            surface = pygame.transform.scale(surface, self.resolution)
            self.screen.blit(surface, (0, 0))

            board = self.automata_update(board)

            while time() - tic < 1/self.max_fps:
                sleep(1/self.max_fps/100)
                self.frametime = time() - tic

            tic = time()

            # Flip the display
            pygame.display.flip()

        print(running)
        # Done! Time to quit.
        pygame.quit()


if __name__ == "__main__":

    def init():
        return np.random.rand(100, 100)

    def update(board):
        return np.random.rand(100, 100)

    viewer = Viewer((200, 200), init, update, 5)
    viewer.run()
