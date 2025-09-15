import pygame
import sys
from Gamestate import GameState

class Game:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.WIN = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.selected = None
        self.state.board.resize(info.current_w, info.current_h)

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            self.WIN.fill((0, 0, 0))
            self.state.board.draw(self.WIN)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.toggle_fullscreen()

                elif event.type == pygame.VIDEORESIZE:
                    self.WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.state.board.resize(event.w, event.h)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    board = self.state.board
                    if board.offset_x <= x < board.offset_x + board.width and board.offset_y <= y < board.offset_y + board.height:
                        col = (x - board.offset_x) // board.square_size
                        row = (y - board.offset_y) // board.square_size
                        piece = board.grid[row][col]

                        if self.selected is None:
                            if piece and piece.color == self.state.turn:
                                self.selected = (row, col)
                        else:
                            sr, sc = self.selected
                            moved = self.state.make_move((sr, sc), (row, col))
                            if moved:
                                self.selected = None
                            else:
                            
                                if piece and piece.color == self.state.turn:
                                    self.selected = (row, col)

if __name__ == "__main__":
    Game().run()
