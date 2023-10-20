from piece import Color

class Game:
    def __init__(self):
        self.winner = None

    
    def count_pieces(self, board):
        reds, blacks = 0, 0
        for i in range(3):
            for j in range(3):
                tile = board.get_tile_from_pos(i*200, j*200)

                if tile.piece is None:
                    continue
                if tile.piece.color == Color.RED:
                    reds += 1
                if tile.piece.color == Color.BLACK:
                    blacks += 1

        return reds, blacks
    

    def no_moves(self, board):
        all_moves = []
        for i in range(3):
            for j in range(3):
                tile = board.get_tile_from_pos(i*200, j*200)

                if tile.piece is not None and tile.piece.color == board.turn:
                    for move in tile.piece.valid_moves():
                        all_moves.append(move)
                    for take in tile.piece.valid_takes():
                        all_moves.append(take)
        if len(all_moves) == 0:
            return Color.BLACK if board.turn == Color.RED else Color.RED
        else:
            return None
        
    

    def check_last_rank(self, board):
        for i in range(3):
            first_row_tile = board.get_tile_from_pos(i * 200, 0)
            last_row_tile = board.get_tile_from_pos(i * 200, 400)

            if first_row_tile.piece is not None and first_row_tile.piece.color == Color.RED:
                return Color.RED
            
            if last_row_tile.piece is not None and last_row_tile.piece.color == Color.BLACK:
                return Color.BLACK
        return None
            

    def check_winner(self, board):
        reds, blacks = self.count_pieces(board)
        last_row_winner = self.check_last_rank(board)
        if reds == 0 or blacks == 0:
            self.winner = Color.RED if reds > blacks else Color.BLACK
            return True
        elif (last_row_winner := self.check_last_rank(board)) is not None:
            self.winner = last_row_winner
            return True
        elif (no_move_winner := self.no_moves(board)) is not None:
            self.winner = no_move_winner
            return True
        else:
            return False
        

    def message(self):
        winner = 'Black' if self.winner == Color.BLACK else 'Red'
        print(f'Winner: {winner}')

                
