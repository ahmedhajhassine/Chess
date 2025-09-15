
from Board import Board

class GameState:
    def __init__(self):
        self.board = Board()
        self.turn = "white"

    def get_piece(self, row, col):
        return self.board.grid[row][col]

    def make_move(self, from_pos, to_pos):
        fr, fc = from_pos
        tr, tc = to_pos
        piece = self.get_piece(fr, fc)
        if piece and piece.color == self.turn:
            valid_moves = self.get_valid_moves(fr, fc)
            if (tr, tc) in valid_moves:
                
                self.board.move_piece(from_pos, to_pos)
                self.turn = "black" if self.turn == "white" else "white"
                return True
        return False

    def get_valid_moves(self, row, col):
       
        piece = self.get_piece(row, col)
        if not piece:
            return []

        if piece.type == "pawn":
            return self.pawn_moves(row, col, piece.color)
        elif piece.type == "rook":
            return self.rook_moves(row, col, piece.color)
        elif piece.type == "knight":
            return self.knight_moves(row, col, piece.color)
        elif piece.type == "bishop":
            return self.bishop_moves(row, col, piece.color)
        elif piece.type == "queen":
            return self.queen_moves(row, col, piece.color)
        elif piece.type == "king":
            return self.king_moves(row, col, piece.color)
        return []

    
    def pawn_moves(self, row, col, color):
        moves = []
        direction = -1 if color == "white" else 1
     
        if self.is_empty(row + direction, col):
            moves.append((row + direction, col))
        
            if (row == 6 and color == "white") or (row == 1 and color == "black"):
                if self.is_empty(row + 2*direction, col):
                    moves.append((row + 2*direction, col))
    
        for dc in [-1, 1]:
            nr, nc = row + direction, col + dc
            if self.is_enemy(nr, nc, color):
                moves.append((nr, nc))
        return moves

    def rook_moves(self, row, col, color):
        return self.straight_moves(row, col, color, [(1,0), (-1,0), (0,1), (0,-1)])

    def bishop_moves(self, row, col, color):
        return self.straight_moves(row, col, color, [(1,1), (1,-1), (-1,1), (-1,-1)])

    def queen_moves(self, row, col, color):
        return self.straight_moves(row, col, color, [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)])

    def king_moves(self, row, col, color):
        moves = []
        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if self.is_empty(nr, nc) or self.is_enemy(nr, nc, color):
                moves.append((nr, nc))
        return moves

    def knight_moves(self, row, col, color):
        moves = []
        jumps = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        for dr, dc in jumps:
            nr, nc = row + dr, col + dc
            if self.is_in_bounds(nr, nc) and (self.is_empty(nr, nc) or self.is_enemy(nr, nc, color)):
                moves.append((nr, nc))
        return moves


    def straight_moves(self, row, col, color, directions):
     
        moves = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            while self.is_in_bounds(nr, nc):
                if self.is_empty(nr, nc):
                    moves.append((nr, nc))
                elif self.is_enemy(nr, nc, color):
                    moves.append((nr, nc))
                    break
                else: 
                    break
                nr += dr
                nc += dc
        return moves

    def is_empty(self, row, col):
        return self.is_in_bounds(row, col) and self.get_piece(row, col) is None

    def is_enemy(self, row, col, color):
        return self.is_in_bounds(row, col) and self.get_piece(row, col) and self.get_piece(row, col).color != color

    def is_in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
