from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os


PIECE_FILES = {
    "br": "br.png", "bn": "bn.png", "bb": "bb.png", "bq": "bq.png", "bk": "bk.png", "bp": "bp.png",
    "wr": "wr.png", "wn": "wn.png", "wb": "wb.png", "wq": "wq.png", "wk": "wk.png", "wp": "wp.png"
}

PIECE_PATH = "/Users/ahmedhajhassine/Desktop/Datateknik/projects/chess/chess/piece/monarchy"

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
        filename = PIECE_FILES.get(self.code)
        if not filename:
            print("No filename for code:", self.code)
            return QPixmap()

        path = os.path.join(PIECE_PATH, filename)
        if not os.path.exists(path):
            print("File not found:", path)
            return QPixmap()


        pixmap = QPixmap(path).scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        return pixmap

    def resize(self, new_size):
        self.size = new_size
        self.surface = self.load_surface()
