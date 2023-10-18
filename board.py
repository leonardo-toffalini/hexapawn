from piece import Piece, Color
from tile import Tile
from pawn import Pawn
import pygame

DEBUG = 3

class Board:
    def __init__(self, board:list[int] = None, turn:Color = Color.BLACK, board_size:int = 600):
        if board is None:
            self.board = [
                [Color.BLACK, Color.BLACK, Color.BLACK],
                [          0,           0,           0],
                [  Color.RED,   Color.RED,   Color.RED]
            ]
        else:
            self.board = board
        self.turn = turn
        self.board_size = board_size
        self.tiles_list = self._generate_tiles()
        self.selected_piece = None


    def _generate_tiles(self):
        tiles_list = []
        for i in range(3):
            for j in range(3):
                new_tile = Tile(i, j, self.board_size//3)
                if j == 0:
                    new_tile.piece = Pawn((i, j), Color.BLACK, self)
                elif j == 2:
                    new_tile.piece = Pawn((i, j), Color.RED, self)
                tiles_list.append(new_tile)
        return tiles_list


    def draw(self, display):
        for tile in self.tiles_list:
            tile.draw(display)
        
        if DEBUG == 1 and self.selected_piece is not None: print(f'position of selected piece: {self.selected_piece.pos}')


    def get_tile_from_pos(self, x, y):
        for tile in self.tiles_list:
            if (tile.x, tile.y) == (x, y):
                return tile

    
    def handle_click(self, pos):
        x, y = pos[0], pos[1]
        x = x // (self.board_size // 3)
        y = y // (self.board_size // 3)
        clicked_tile = self.get_tile_from_pos(x * (self.board_size // 3), y * (self.board_size // 3))

        if DEBUG == 2: print(f'clicked tile: {clicked_tile}')

        if self.selected_piece is None and clicked_tile.piece is not None and clicked_tile.piece.color == self.turn:
            self.selected_piece = clicked_tile.piece

        elif self.selected_piece is not None and self.selected_piece.move(clicked_tile):
            self.turn = Color.BLACK if self.turn == Color.RED else Color.RED
        if DEBUG == 3: print(f'turn: {self.turn}')

        elif clicked_tile.piece is not None and clicked_tile.piece.color == self.turn:
            self.selected_piece = clicked_tile.piece

        for tile in self.tiles_list:
            tile.highlight = False
        clicked_tile.highlight = True


def main():
    my_board = Board()

    board_size = 600

    pygame.init()
    screen = pygame.display.set_mode((board_size, board_size))
    running = True
    
    while running:
        my_board.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
               my_board.handle_click(event.pos) 

    pygame.quit()

if __name__ == '__main__':
    main()