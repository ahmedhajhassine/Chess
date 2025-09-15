import pygame
from Piece import Piece

ROWS, COLS = 8, 8
WHITE = (245, 245, 220)
BROWN = (139, 69, 19)

START_POSITION = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wr","wn","wb","wq","wk","wb","wn","wr"]
]

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.square_size = 80
        self.offset_x = 0
        self.offset_y = 0
        self.width = self.height = self.square_size * COLS
        self.load_start_position()

    def load_start_position(self):
        for r in range(ROWS):
            for c in range(COLS):
                code = START_POSITION[r][c]
                if code != ".":
                    self.grid[r][c] = Piece(code, self.square_size)

    def draw(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BROWN
                rect = pygame.Rect(self.offset_x + col*self.square_size,
                                   self.offset_y + row*self.square_size,
                                   self.square_size, self.square_size)
                pygame.draw.rect(win, color, rect)
                piece = self.grid[row][col]
                if piece:
                    win.blit(piece.surface, (self.offset_x + col*self.square_size,
                                             self.offset_y + row*self.square_size))

    def resize(self, screen_width, screen_height):
        board_size = int(min(screen_width, screen_height) * 0.8)
        self.square_size = board_size // 8
        self.width = self.height = self.square_size * 8
        self.offset_x = (screen_width - self.width) // 2
        self.offset_y = (screen_height - self.height) // 2
        # Resize all pieces
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.grid[r][c]
                if piece:
                    piece.resize(self.square_size)

    def move_piece(self, from_pos, to_pos):
        fr, fc = from_pos
        tr, tc = to_pos
        if self.grid[fr][fc]:
            self.grid[tr][tc] = self.grid[fr][fc]
            self.grid[fr][fc] = None