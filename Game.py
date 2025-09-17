import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QSizePolicy
)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt, QRect, QSize

from Piece import Piece
from Board import Board
from Gamestate import GameState


class BoardCanvas(QWidget):
    def __init__(self, board, parent=None):
        super().__init__(parent)
        self.board = board
        self.selected = None
        self.legal_moves = []
        self.last_move = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Compute board size and offsets
        side = min(self.width(), self.height()) - 50
        offset_x = (self.width() - side) // 2
        offset_y = (self.height() - side) // 2
        square_size = side // 8
        self.board.square_size = square_size

        # Draw squares
        for row in range(8):
            for col in range(8):
                color = QColor(238, 238, 210) if (row + col) % 2 == 0 else QColor(118, 150, 86)
                rect = QRect(int(offset_x + col*square_size),
                             int(offset_y + row*square_size),
                             int(square_size), int(square_size))
                painter.fillRect(rect, color)

        # Highlight last move squares
        if hasattr(self.board, 'last_move') and self.board.last_move:
            (sr1, sc1), (sr2, sc2) = self.board.last_move
            highlight_color = QColor(97, 38, 42, 120)
            radius = int(square_size * 0.45)
            for r, c in [(sr1, sc1), (sr2, sc2)]:
                center_x = int(offset_x + c*square_size + square_size/2)
                center_y = int(offset_y + r*square_size + square_size/2)
                painter.setBrush(highlight_color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)

        # Highlight selected square
        if self.selected:
            sr, sc = self.selected
            rect = QRect(int(offset_x + sc*square_size),
                         int(offset_y + sr*square_size),
                         int(square_size), int(square_size))
            painter.fillRect(rect, QColor(255, 255, 0, 120))  # transparent yellow

        # Highlight legal moves
        if self.selected and self.legal_moves:
            radius_outer = int(square_size * 0.5)
            radius_inner = int(square_size * 0.4)
            radius_inner_nc = int(square_size * 0.2)
            green_color = QColor(120, 135, 100, 140)
            gray_color = QColor(75, 72, 71, 140)

            for r, c in self.legal_moves:
                center_x = int(offset_x + c*square_size + square_size/2)
                center_y = int(offset_y + r*square_size + square_size/2)
                target_piece = self.board.grid[r][c]

                if target_piece and target_piece.color != self.board.grid[self.selected[0]][self.selected[1]].color:
                    # Hollow capture circle
                    painter.setBrush(gray_color)
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(center_x - radius_outer, center_y - radius_outer, radius_outer*2, radius_outer*2)

                    # Inner circle with square color
                    square_color = QColor(238, 238, 210)if (r + c) % 2 == 0 else QColor(118, 150, 86) 
                    painter.setBrush(square_color)
                    painter.drawEllipse(center_x - radius_inner, center_y - radius_inner, radius_inner*2, radius_inner*2)
                else:
                    # Regular legal move
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(green_color)
                    painter.drawEllipse(center_x - radius_inner_nc, center_y - radius_inner_nc, radius_inner_nc*2, radius_inner_nc*2)

        # Draw pieces crisply
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece:
                    # Resize piece pixmap if needed
                    if piece.size != square_size:
                        piece.resize(square_size)
                    rect = QRect(int(offset_x + col*square_size),
                                 int(offset_y + row*square_size),
                                 int(square_size), int(square_size))
                    painter.drawPixmap(rect, piece.surface)

    def mousePressEvent(self, event):
        side = min(self.width(), self.height()) - 50
        offset_x = (self.width() - side) // 2
        offset_y = (self.height() - side) // 2
        square_size = side // 8

        x, y = event.position().x() - offset_x, event.position().y() - offset_y
        col = int(x // square_size)
        row = int(y // square_size)
        if 0 <= row < 8 and 0 <= col < 8:
            self.window().handle_click(row, col)
            self.update()


class ChessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess PySide6")
        self.state = GameState()
        self.fullscreen = False

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Board
        self.board_canvas = BoardCanvas(self.state.board, self)
        main_layout.addWidget(self.board_canvas, stretch=3)

        # Buttons
        button_panel = QWidget()
        button_layout = QVBoxLayout()
        button_panel.setLayout(button_layout)
        main_layout.addWidget(button_panel, stretch=1)

        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(self.new_game)
        button_layout.addWidget(new_game_button)

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.settings)
        button_layout.addWidget(settings_button)

        fullscreen_button = QPushButton("Toggle Fullscreen")
        fullscreen_button.clicked.connect(self.toggle_fullscreen)
        button_layout.addWidget(fullscreen_button)

        button_layout.addStretch()

        self.resize(1600, 1000)

    def handle_click(self, row, col):
        piece = self.state.board.grid[row][col]
        if self.board_canvas.selected is None:
            if piece and piece.color == self.state.turn:
                self.board_canvas.selected = (row, col)
                self.board_canvas.legal_moves = self.state.get_valid_moves(row, col)
        else:
            sr, sc = self.board_canvas.selected
            moved = self.state.make_move((sr, sc), (row, col))
            if moved:
                self.board_canvas.last_move = ((sr, sc), (row, col))
                self.board_canvas.selected = None
            else:
                if piece and piece.color == self.state.turn:
                    self.board_canvas.selected = (row, col)
                    self.board_canvas.legal_moves = self.state.get_valid_moves(row, col)
        self.board_canvas.update()

    def new_game(self):
        reply = QMessageBox.question(self, "New Game", "Start a new game?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.state = GameState()
            self.board_canvas.board = self.state.board
            self.board_canvas.selected = None
            self.board_canvas.update()

    def settings(self):
        QMessageBox.information(self, "Settings", "Settings menu (not implemented)")

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.showNormal()
            self.fullscreen = False
        else:
            self.showFullScreen()
            self.fullscreen = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessWindow()
    window.show()
    sys.exit(app.exec())
