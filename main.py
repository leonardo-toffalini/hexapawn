import pygame
from board import Board
from game import Game

pygame.init()

class Hexapawn:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.FPS = pygame.time.Clock()


    def _draw(self, board: Board) -> None:
        """ Draws the board """
        board.draw(self.screen)
        pygame.display.update()


    def main(self, board_size: int, num_tiles: int = 3) -> None:
        """ Main game loop """
        board = Board(board_size=board_size, board = None, num_tiles=num_tiles)
        game = Game(board)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if not game.check_winner():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        board.handle_click(event.pos[0], event.pos[1]) 
                else:
                    game.message()
                    self.running = False
            self._draw(board)
            self.FPS.tick(60)


def main():
    board_size = 600
    num_tiles = 3

    screen = pygame.display.set_mode((board_size, board_size))
    pygame.display.set_caption('Hexapawn')

    hexapawn = Hexapawn(screen)
    hexapawn.main(board_size, num_tiles)

    pygame.quit()

if __name__ == '__main__':
    main()