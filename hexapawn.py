import copy
from time import time

class Board():
    def __init__(self, board:bool=None, turn:int=1):
        if board == None:
            self.board = [
                [-1, -1, -1],
                [0,  0,  0],
                [1,  1,  1]
            ]
        else:
            self.board = board

        self.turn = turn


    def _convert(self, x:int) -> str:
        if x == 1:
            return "X"
        elif x == -1:
            return "O"
        elif x == 0:
            return " "


    def _hash_pos(self):
        result = ""
        for i in range(3):
            for j in range(3):
                result += self._convert(self.board[i][j])
        return result


    def displayBoard(self) -> None:
        print(f'{self._convert(self.board[0][0])}|{self._convert(self.board[0][1])}|{self._convert(self.board[0][2])}')
        print('------')
        print(f'{self._convert(self.board[1][0])}|{self._convert(self.board[1][1])}|{self._convert(self.board[1][2])}')
        print('------')
        print(f'{self._convert(self.board[2][0])}|{self._convert(self.board[2][1])}|{self._convert(self.board[2][2])}')


    def getMoves(self, row:int, col:int) -> list:
        moves = []
        # preliminary check
        if self.board[row][col] == self.turn:
            if row-self.turn in range(3) and col in range(3) and self.board[row-self.turn][col] == 0:
                moves.append((row-self.turn, col))
            if row-self.turn in range(3) and col-1 in range(3) and self.board[row-self.turn][col-1] == -self.turn:
                moves.append((row-self.turn, col-1))
            if row-self.turn in range(3) and col+1 in range(3) and self.board[row-self.turn][col+1] == -self.turn:
                moves.append((row-self.turn, col+1))

        return moves


    def move(self, row:int, col:int, newRow:int, newCol:int):
        moves = dict()
        for i in range(3):
            for j in range(3):
                moves[(i, j)] = self.getMoves(i, j)
        # print(moves)
        if (newRow, newCol) in moves[(row, col)]:
            self.board[row][col] = 0
            self.board[newRow][newCol] = self.turn
            self.turn = -self.turn
        else:
            print("Invalid move")


    def checkWinner(self) -> int:
        for j in range(3):
            if self.board[0][j] == 1:
                return 1
            if self.board[-1][j] == -1:
                return -1

        moves = dict()
        for i in range(3):
            for j in range(3):
                if (move:=self.getMoves(i, j)):
                    moves[(i, j)] = move

        if len(moves) == 0:
            return -self.turn

        return 0


    def minimax(self, depth:int, player:int) -> float:
        moves = dict()
        for i in range(3):
            for j in range(3):
                if (move := self.getMoves(i, j)):
                    moves[(i, j)] = move

        if player == 1:
            value = -float('inf')
            for key in moves:
                for val in moves[key]:
                    child = Board(copy.deepcopy(self.board), self.turn)
                    child.move(key[0], key[1], val[0], val[1])
                    score = child.minimax(depth-1, -player)
                    value = max(value, score)
            return value

        else:
            value = float('inf')
            for key in moves:
                for val in moves[key]:
                    child = Board(copy.deepcopy(self.board), self.turn)
                    child.move(key[0], key[1], val[0], val[1])
                    score = child.minimax(depth-1, -player)
                    value = min(value, score)
            return value


    def alphabeta(self, depth:int, alpha:float, beta:float, player:int) -> float:
        look_up_table = dict()
        print(look_up_table)

        moves = dict()
        for i in range(3):
            for j in range(3):
                if (move := self.getMoves(i, j)):
                    moves[(i, j)] = move

        if player == 1:
            value = -float('inf')
            for key in moves:
                for val in moves[key]:
                    child = Board(copy.deepcopy(self.board), self.turn)
                    child.move(key[0], key[1], val[0], val[1])
                    # look up the position in the look up table or store it if its not in it
                    if (hashed_pos := child._hash_pos()) in look_up_table:
                        score = look_up_table[hashed_pos]
                    else:
                        score = child.alphabeta(depth-1, alpha, beta, -player)
                        look_up_table[hashed_pos] = score
                    value = max(value, score)
                    if value > beta:
                        break
                    alpha = max(alpha, value)
            return value

        else:
            value = float('inf')
            for key in moves:
                for val in moves[key]:
                    child = Board(copy.deepcopy(self.board), self.turn)
                    child.move(key[0], key[1], val[0], val[1])
                    # look up the position in the look up table or store it if its not in it
                    if (hashed_pos := child._hash_pos()) in look_up_table:
                        score = look_up_table[hashed_pos]
                    else:
                        score = child.alphabeta(depth-1, alpha, beta, -player)
                        look_up_table[hashed_pos] = score
                    value = min(value, score)
                    if value < alpha:
                        break
                    beta = min(beta, value)
            return value


    def get_best_move(self, depth:int, player:int, ab:bool=False):
        moves = dict()
        for i in range(3):
            for j in range(3):
                if (move := self.getMoves(i, j)):
                    moves[(i, j)] = move

        if player == 1:
            value = -float('inf')
        elif player == -1:
            value = float('inf')

        best_move = -1

        for key in moves:
            for val in moves[key]:
                child = Board(copy.deepcopy(self.board), self.turn)
                child.move(key[0], key[1], val[0], val[1])
                if ab:
                    score = child.alphabeta(depth, -float('inf'), float('inf'), -player)
                else:
                    score = child.minimax(depth, -player)
                curr_move = (key[0], key[1], val[0], val[1])

                if player == 1 and score > value:
                    value, best_move = score, curr_move
                elif player == -1 and score < value:
                    value, best_move = score, curr_move
        
        return "you already lost" if best_move == -1 else best_move



def main():
    board = Board()
    while True:
        # t1 = time()
        # print(board.minimax(5, 1))
        # print(f'it took {time()-t1} seconds')
        # t2 = time()
        # print(board.alphabeta(5, -float('inf'), float('inf'), 1))
        # print(f'it took {time()-t2} seconds')
        # print(board._hash_pos())
        t3 = time()
        print(board.get_best_move(5, board.turn, ab=True))
        print(time() - t3)

        board.displayBoard()

        row = int(input("Input row "))
        col = int(input("Input col "))
        newRow = int(input("Input newRow "))
        newCol = int(input("Input newCol "))

        board.move(row, col, newRow, newCol)

        if board.checkWinner():
            print(board._convert(board.checkWinner()))
            break


if __name__ == '__main__':
    main()