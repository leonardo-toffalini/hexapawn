from enum import Enum
from typing import Tuple
import pygame
from tile import Tile

DEBUG = 0


class Color(Enum):
    BLACK = -1
    RED = 1


class Piece:
    def __init__(self, pos: tuple[int, int], color: Color, board):
        self.pos = pos
        self.color = color
        self.board = board
        self.img: pygame.surface.Surface

    def move(self, tile: Tile) -> bool:
        """Moves the pawn to the specified tile if applicable, returns True if move was applicable, returns False otherwise"""
        move = (tile.y_index - self.pos[0], tile.x_index - self.pos[1])  # (row, col)

        if move in self.valid_moves():
            prev = self.board.get_tile_from_pos(self.pos[1], self.pos[0])
            self.board.board[self.pos[0]][self.pos[1]] = 0
            self.pos = (tile.y_index, tile.x_index)
            prev.piece = None
            tile.piece = self
            self.board.board[tile.y_index][tile.x_index] = self.color
            self.board.selected_piece = None
            return True

        if move in self.valid_takes():
            prev = self.board.get_tile_from_pos(self.pos[1], self.pos[0])
            self.board.board[self.pos[0]][self.pos[1]] = 0
            self.pos = (tile.y_index, tile.x_index)
            prev.piece = None
            tile.piece = self
            self.board.board[tile.y_index][tile.x_index] = self.color
            self.board.selected_piece = None
            return True

        else:
            self.board.selected_piece = None
            return False

    def valid_moves(self) -> Tuple[int, int]:
        return (0, 0)

    def valid_takes(self) -> Tuple[int, int]:
        return (0, 0)
