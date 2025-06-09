import pygame
from ai import minimax
from chess_rules import get_piece_moves, is_in_check
from pgn import move_to_pgn, pos_to_alg
from utils import load_images

class ChessGame:
    check_alert_font = None
    def __init__(self, screen, ai_depth):
        self.screen = screen
        self.board = self.create_starting_board()
        self.selected = None
        self.turn = 'w'
        self.valid_moves = []
        self.ai_depth = ai_depth
        self.pgn_moves = []
        self.move_number = 1
        self.images = load_images()
        self.game_over = False
        if ChessGame.check_alert_font is None:
            ChessGame.check_alert_font = pygame.font.SysFont(None, 48)
        self.check_alert = False

    def create_starting_board(self):
        return [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP']*8,
            [None]*8,
            [None]*8,
            [None]*8,
            [None]*8,
            ['wP']*8,
            ['wR','wN','wB','wQ','wK','wB','wN','wR'],
        ]

    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Atualiza alerta de xeque
            self.check_alert = is_in_check(self.board, self.turn)
            self.draw()
            if self.turn == 'b' and not self.game_over:
                _, move = minimax(self.board, self.ai_depth, False)
                if move:
                    self.make_move(*move)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // 80, x // 80
                    if self.selected:
                        if (row, col) in self.valid_moves:
                            self.make_move(self.selected, (row, col))
                            self.selected = None
                            self.valid_moves = []
                        else:
                            self.selected = None
                            self.valid_moves = []
                    else:
                        piece = self.board[row][col]
                        if piece and piece[0] == self.turn:
                            self.selected = (row, col)
                            self.valid_moves = self.get_valid_moves(row, col)

            clock.tick(30)

    def draw(self):
        colors = [(240,217,181), (181,136,99)]
        for row in range(8):
            for col in range(8):
                color = colors[(row+col)%2]
                pygame.draw.rect(self.screen, color, (col*80, row*80, 80, 80))
                if self.selected and (row, col) in self.valid_moves:
                    pygame.draw.rect(self.screen, (0,255,0), (col*80, row*80, 80, 80), 3)
                piece = self.board[row][col]
                if piece:
                    self.screen.blit(self.images[piece], (col*80, row*80))
        # Alerta de xeque
        if self.check_alert:
            alert_text = ChessGame.check_alert_font.render('XEQUE!', True, (255,0,0))
            self.screen.blit(alert_text, (320 - alert_text.get_width()//2, 10))
        pygame.display.flip()

    def get_valid_moves(self, row, col):
        # Movimentos reais de xadrez
        return get_piece_moves(self.board, row, col)

    def make_move(self, start, end):
        piece = self.board[start[0]][start[1]]
        captured = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        notation = move_to_pgn(piece, start, end, capture=bool(captured))
        if self.turn == 'w':
            self.pgn_moves.append(f"{self.move_number}. {notation}")
        else:
            self.pgn_moves[-1] += f" {notation}"
            self.move_number += 1

        self.turn = 'b' if self.turn == 'w' else 'w'
