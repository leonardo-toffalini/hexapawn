from game import Game
from piece import Color


class Engine:
    def __init__(self, game: Game):
        self.game = game

    def evaluate(self):
        if self.game.check_winner():
            return (
                float("inf")
                if self.game.winner == self.game.board.turn
                else -float("inf")
            )

    def all_moves(self):
        """Retruns a dictionary of the form: Tile at (row, col) -> list[moves for piece at (row, col)]"""
        all_moves = dict()
        for i in range(self.game.board.num_tiles):
            for j in range(self.game.board.num_tiles):
                tile = self.game.board.get_tile_from_pos(
                    j, i
                )  # expects parameters col, row

                if tile.piece is not None and tile.piece.color == self.game.board.turn:
                    for moves in tile.piece.valid_moves():
                        all_moves[(i, j)] = moves
                    for takes in tile.piece.valid_takes():
                        all_moves[(i, j)] = takes
        return all_moves

    def minimax(self, depth: int = 9):
        pass

    def alphabeta(
        self,
        depth: int = 9,
        player: Color = Color.RED,
        alpha: float = -float("inf"),
        beta: float = float("inf"),
    ):
        pass
