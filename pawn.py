import pygame
from piece import Piece, Color
from tile import Tile


class Pawn(Piece):
    def __init__(self, pos: tuple[int, int], color: Color, board):
        super().__init__(pos, Color, board)
        img_path = 'images/black-pawn.png' if color == Color.BLACK else 'images/red-pawn.png'
        self.board = board
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (200, 200))

    def _possible_moves(self):
        return [(0, 1)] if self.color == Color.BLACK else [(0, -1)]
    

    def _possible_takes(self):
        return [(-1, 1), (1, 1)] if self.color == Color.BLACK else [(-1, -1), (1, -1)]


    def valid_moves(self):
        moves = []
        poss_moves = self._possible_moves()
        for move in poss_moves:
            tile_pos = (self.pos[0] + move[0], self.pos[1] + move[1])
            print(f'tile pos = {tile_pos}')
            if tile_pos[0] > 2 or tile_pos[0] < 0 or tile_pos[1] > 2 or tile_pos[1] < 0:
                continue
            
            tile = self.board.get_tile_from_pos(tile_pos[0] * (self.board.board_size // 3), tile_pos[1] * (self.board.board_size // 3))
            if tile.piece is None:
                moves.append(move)
        return moves

    
    def valid_takes(self):
        takes = []
        poss_takes = self._possible_takes()
        for take in poss_takes:
            tile_pos = (self.pos[0] + take[0], self.pos[1] + take[1])
            if tile_pos[0] > 2 or tile_pos[0] < 0 or tile_pos[1] > 2 or tile_pos[1] < 0:
                continue
            
            tile = self.board.get_tile_from_pos(tile_pos[0] * (self.board.board_size // 3), tile_pos[1] * (self.board.board_size // 3))
            if tile.piece is not None and tile.piece.color == -self.color:
                takes.append(take)
        return takes


    def move(self, tile: Tile):
        valid_moves = self.valid_moves()
        print(f'valid moves: {valid_moves}')
        # print(f'tile.x = {tile.x}')
        print(f'direction: {(tile.x//200) - self.pos[0], (tile.y//200) - self.pos[1]}')
        if ((tile.x//200) - self.pos[0], (tile.y//200) - self.pos[1]) in self.valid_moves():
            prev = tile
            self.pos = (tile.x, tile.y)
            prev.piece = None
            tile.piece = self
            self.board.selected_piece = None
            return True

        if tile in self.valid_takes():
            prev = tile
            self.pos = (tile.x ,tile.y)
            prev.piece = None
            tile.piece = self
            self.board.selected_piece = None
            return True

        else:
            self.board.selected_piece = None
            return False
