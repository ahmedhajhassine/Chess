import pygame
import os
import io
import cairosvg

PIECE_FILES = {
    "br": "bR.svg", "bn": "bN.svg", "bb": "bB.svg", "bq": "bQ.svg", "bk": "bK.svg", "bp": "bP.svg",
    "wr": "wR.svg", "wn": "wN.svg", "wb": "wB.svg", "wq": "wQ.svg", "wk": "wK.svg", "wp": "wP.svg"
}
PIECE_PATH = "/Users/ahmedhajhassine/Desktop/Datateknik/projects/chess/chess/data/lila-master/public/piece/alpha"

class Piece:
    def __init__(self, code, size):
        self.code = code
        self.color = "white" if code[0] == "w" else "black"
        self.type = self._map_type(code[1])
        self.size = size
        self.surface = self.load_surface()

    def _map_type(self, char):
        mapping = {
            "p": "pawn",
            "r": "rook",
            "n": "knight",
            "b": "bishop",
            "q": "queen",
            "k": "king"
        }
        return mapping.get(char, "unknown")

    def load_surface(self):
        filename = PIECE_FILES[self.code]
        path = os.path.join(PIECE_PATH, filename)
        png_data = cairosvg.svg2png(url=path, output_width=self.size, output_height=self.size)
        return pygame.image.load(io.BytesIO(png_data)).convert_alpha()

    def resize(self, new_size):
        self.size = new_size
        self.surface = self.load_surface()