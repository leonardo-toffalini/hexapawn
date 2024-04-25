import pygame
from board import Board
from game import Game
from piece import Color
from engine import Engine

pygame.init()


class Hexapawn:
    def __init__(self, screen: pygame.surface.Surface, players=2):
        self.screen = screen
        self.running = True
        self.FPS = pygame.time.Clock()
        self.players = players

    def _draw(self, board: Board) -> None:
        """Draws the board"""
        board.draw(self.screen)
        pygame.display.update()

    def main(self, board_size: int, num_tiles: int = 3) -> None:
        """Main game loop"""
        board = Board(board_size=board_size, board=None, num_tiles=num_tiles)
        game = Game(board)
        engine = Engine(game)

        if self.players == 2:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type == pygame.KEYDOWN:
                        clone_board = Board(
                            board_size=board_size,
                            board=board.board,
                            num_tiles=num_tiles,
                        )
                        clone_game = Game(clone_board)
                        print(clone_board.board)
                        print(clone_game.minimax())

                    if not game.check_winner():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            board.handle_click(*pos)
                    else:
                        game.message()
                        self.running = False
                self._draw(board)
                self.FPS.tick(60)

        if self.players == 1:
            while self.running:
                if board.turn == "X":
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False

                        if event.type == pygame.MOUSEBUTTONUP:
                            pos = pygame.mouse.get_pos()
                            board.handle_click(*pos)
                else:
                    move = engine.alphabeta(player=Color.RED, depth=9)
                    game.make_move(move[0], move[1], "O")
                    board.turn = "X"

                if game.check_winner() is not None:
                    if (winner := game.check_winner()) in ["O", "X"]:
                        print(f"Winner: {winner}")
                    else:
                        print("Tie")
                    self.running = False

                self._draw(board)
                pygame.display.update()


def main():
    board_size = 600
    num_tiles = 3

    screen = pygame.display.set_mode((board_size, board_size))
    pygame.display.set_caption("Hexapawn")

    hexapawn = Hexapawn(screen)
    hexapawn.main(board_size, num_tiles)

    pygame.quit()


if __name__ == "__main__":
    main()
