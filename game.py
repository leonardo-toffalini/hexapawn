from typing import Tuple
from piece import Color
from pawn import Pawn


class Game:
    def __init__(self, board):
        self.winner = None
        self.board = board

    def count_pieces(self) -> Tuple[int, int]:
        """Returns the number of black and red pieces on the board"""
        reds, blacks = 0, 0
        for i in range(self.board.num_tiles):
            for j in range(self.board.num_tiles):
                tile = self.board.get_tile_from_pos(j, i)

                if tile.piece is None:
                    continue
                if tile.piece.color == Color.RED:
                    reds += 1
                if tile.piece.color == Color.BLACK:
                    blacks += 1

        return reds, blacks

    def no_moves(self) -> Color | None:
        """Returns the RED if BLACK has no legal moves or BLACK if RED has no legal moves, None otherwise"""
        all_moves = []
        for i in range(self.board.num_tiles):
            for j in range(self.board.num_tiles):
                tile = self.board.get_tile_from_pos(j, i)

                if tile.piece is not None and tile.piece.color == self.board.turn:
                    for move in tile.piece.valid_moves():
                        all_moves.append(move)
                    for take in tile.piece.valid_takes():
                        all_moves.append(take)
        if len(all_moves) == 0:
            return Color.BLACK if self.board.turn == Color.RED else Color.RED
        else:
            return None

    def check_last_rank(self) -> Color | None:
        """Returns BLACK if a BLACK piece has reached the last rank, returns RED if a RED piece has reached the last rank, returns None otherwise"""
        for i in range(self.board.num_tiles):
            first_row_tile = self.board.get_tile_from_pos(i, 0)
            last_row_tile = self.board.get_tile_from_pos(i, self.board.num_tiles - 1)

            if (
                first_row_tile.piece is not None
                and first_row_tile.piece.color == Color.RED
            ):
                return Color.RED

            if (
                last_row_tile.piece is not None
                and last_row_tile.piece.color == Color.BLACK
            ):
                return Color.BLACK
        return None

    def check_winner(self) -> bool:
        """Returns True if any player has won, returns False otherwise"""
        reds, blacks = self.count_pieces()
        last_row_winner = self.check_last_rank()
        if reds == 0 or blacks == 0:
            self.winner = Color.RED if reds > blacks else Color.BLACK
            return True
        elif (last_row_winner := self.check_last_rank()) is not None:
            self.winner = last_row_winner
            return True
        elif (no_move_winner := self.no_moves()) is not None:
            self.winner = no_move_winner
            return True
        else:
            return False

    def message(self):
        """Prints out the winner"""
        winner = "Black" if self.winner == Color.BLACK else "Red"
        print(f"Winner: {winner}")

    def make_move(self, from_row, from_col, to_row, to_col, color):
        tile = self.board.get_tile_from_pos(from_col, from_row)
        to_tile = self.board.get_tile_from_pos(to_col, to_row)
        tile.piece = None
        # self.board.board[from_row][from_col] = 0
        to_tile.piece = Pawn((to_row, to_col), color, self.board, self.board.tile_size)
        # self.board.board[to_row][to_col] = color

    def unmake_move(self, from_row, from_col, to_row, to_col, was_take, color):
        tile = self.board.get_tile_from_pos(from_col, from_row)
        to_tile = self.board.get_tile_from_pos(to_col, to_row)
        if not was_take:
            tile.piece = None
            # self.board.board[from_row][from_col] = 0
            to_tile.piece = Pawn(
                (to_row, to_col), color, self.board, self.board.tile_size
            )
            # self.board.board[to_row][to_col] = color

        if was_take:
            other_color = Color.BLACK if color == Color.RED else Color.RED
            tile.piece = Pawn(
                (from_row, from_col), other_color, self.board, self.board.tile_size
            )
            # self.board.board[from_row][from_col] = other_color
            to_tile.piece = Pawn(
                (to_row, to_col), color, self.board, self.board.tile_size
            )
            # self.board.board[to_row][to_col] = color

    def get_moves(self):
        all_moves = []
        for i in range(self.board.num_tiles):
            for j in range(self.board.num_tiles):
                tile = self.board.get_tile_from_pos(j, i)

                if tile.piece is not None and tile.piece.color == self.board.turn:
                    for move in tile.piece.valid_moves():
                        all_moves.append((i, j, i + move[0], j + move[1], False))
                    for take in tile.piece.valid_takes():
                        all_moves.append((i, j, i + take[0], j + take[1], True))
        return all_moves

    def evaluate(self):
        reds, blacks = self.count_pieces()
        if reds == 0:
            return -10
        if blacks == 0:
            return 10

        if (last_row_winner := self.check_last_rank()) is not None:
            return 10 if last_row_winner == Color.RED else -10
        if (no_move_winner := self.no_moves()) is not None:
            return 10 if no_move_winner == Color.RED else -10

        return False

    def minimax(self, player: Color = Color.RED, depth: int = 9):
        if player == Color.RED:
            best = [-1, -1, -1, -1, -10]
        else:
            best = [-1, -1, -1, -1, 10]

        if depth == 0 or self.check_winner():
            score = [
                -1,
                -1,
                -1,
                -1,
                self.evaluate(),
            ]  # from_row, from_col, to_row, to_col, score
            return score

        for move in self.get_moves():
            from_row, from_col, to_row, to_col, take = move
            self.make_move(from_row, from_col, to_row, to_col, player)  # make the move
            score = self.minimax(
                Color.RED if player == Color.BLACK else Color.BLACK, depth - 1
            )
            self.unmake_move(
                to_row, to_col, from_row, from_col, player, take
            )  # undo the move
            score[0], score[1], score[2], score[3] = from_row, from_col, to_row, to_col

            if player == Color.RED:
                if score[-1] > best[-1]:
                    best = score
            else:
                if score[-1] < best[-1]:
                    best = score

        return best
