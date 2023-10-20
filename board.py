from piece import Piece, Color
from tile import Tile
from pawn import Pawn, DEBUG
import pygame

class Board:
    def __init__(self, turn:Color = Color.RED, board_size:int = 600, num_tiles=3):
        self.turn = turn
        self.board_size = board_size
        self.num_tiles = num_tiles
        self.tile_size = self.board_size // self.num_tiles
        self.tiles_list = self._generate_tiles()
        self.selected_piece = None


    def _generate_tiles(self):
        tiles_list = []
        for i in range(self.num_tiles):
            for j in range(self.num_tiles):
                new_tile = Tile(i, j, self.tile_size)
                if j == 0:
                    new_tile.piece = Pawn((i, j), Color.BLACK, self, self.tile_size)
                elif j == self.num_tiles - 1:
                    new_tile.piece = Pawn((i, j), Color.RED, self, self.tile_size)
                tiles_list.append(new_tile)
        return tiles_list


    def draw(self, display):
        for tile in self.tiles_list:
            tile.draw(display)
        
        if DEBUG >= 1 and self.selected_piece is not None: print(f'position of selected piece: {self.selected_piece.pos}')


    def get_tile_from_pos(self, x, y):
        for tile in self.tiles_list:
            if (tile.x_index, tile.y_index) == (x, y):
                return tile

    
    def handle_click(self, pos):
        x, y = pos[0], pos[1]
        x = x // self.tile_size
        y = y // self.tile_size
        clicked_tile = self.get_tile_from_pos(x, y)
        if DEBUG >= 2: print(f'clicked tile pos: {clicked_tile}')

        if DEBUG >= 2: print(f'clicked tile: {clicked_tile}')
        if DEBUG >= 2: print(f'selected piece: {self.selected_piece}')
        if DEBUG >= 2: print(f'clicked tile piece: {clicked_tile.piece}')
        if DEBUG >= 2: print(f'clicked tile piece color: {clicked_tile.piece}')
        if DEBUG >= 2: print(f'turn: {self.turn}')

        if self.selected_piece is None and clicked_tile.piece is not None and clicked_tile.piece == self.turn:
            self.selected_piece = clicked_tile.piece

        elif self.selected_piece is not None and self.selected_piece.move(clicked_tile):
            self.turn = Color.BLACK if self.turn == Color.RED else Color.RED

        elif clicked_tile.piece is not None and clicked_tile.piece.color == self.turn:
            self.selected_piece = clicked_tile.piece

        for tile in self.tiles_list:
            tile.highlight = False
        clicked_tile.highlight = True
