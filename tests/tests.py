# fmt: off
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
# fmt: on
from cellular_automata import Board


def test_from_stencils():
    for idx in range(10):
        board = Board.random(20)
        assert board == Board.from_stencils(board.stencil_form())