

import pygame
from ai import minimax
from chess_rules import get_piece_moves, is_in_check
from pgn import move_to_pgn, pos_to_alg
from utils import load_images
import copy

class ChessGame:
    def get_best_move(self):
        from ai import get_all_moves, evaluate
        import copy
        moves = get_all_moves(self.board, self.turn)
        if not moves:
            return None, None
        best_score = None
        best_move = None
        reverse = self.turn == 'w'
        for move in moves:
            new_board = copy.deepcopy(self.board)
            TrainingChessGame.apply_move_static(new_board, move)
            score = evaluate(new_board)
            if best_score is None or (reverse and score > best_score) or (not reverse and score < best_score):
                best_score = score
                best_move = move
        return best_move, best_score
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
        files = 'abcdefgh'
        ranks = '87654321'
        # Tabuleiro
        for row in range(8):
            for col in range(8):
                color = colors[(row+col)%2]
                pygame.draw.rect(self.screen, color, (col*80, row*80, 80, 80))
                if self.selected and (row, col) in self.valid_moves:
                    pygame.draw.rect(self.screen, (0,255,0), (col*80, row*80, 80, 80), 3)
                piece = self.board[row][col]
                if piece:
                    self.screen.blit(self.images[piece], (col*80, row*80))
        # Letras (a-h) abaixo
        font_letnum = pygame.font.SysFont(None, 24)
        for i in range(8):
            let = font_letnum.render(files[i], True, (0,0,0))
            self.screen.blit(let, (i*80 + 40 - let.get_width()//2, 640-20))
        # Números (1-8) à esquerda
        for i in range(8):
            num = font_letnum.render(ranks[i], True, (0,0,0))
            self.screen.blit(num, (5, i*80 + 40 - num.get_height()//2))
        # Melhor jogada e destaque visual
        best_move, best_score = self.get_best_move()
        if best_move:
            from pgn import move_to_pgn
            piece = self.board[best_move[0][0]][best_move[0][1]]
            notation = move_to_pgn(piece, best_move[0], best_move[1], capture=self.board[best_move[1][0]][best_move[1][1]] is not None)
            # Nome da peça
            piece_names = {'P': 'Peão', 'N': 'Cavalo', 'B': 'Bispo', 'R': 'Torre', 'Q': 'Rainha', 'K': 'Rei'}
            nome_peca = piece_names.get(piece[1], piece[1])
            # Mensagem clara de qual peça mover
            pos_letras = 'abcdefgh'
            pos_numeros = '87654321'
            casa_origem = f"{pos_letras[best_move[0][1]]}{pos_numeros[best_move[0][0]]}"
            casa_destino = f"{pos_letras[best_move[1][1]]}{pos_numeros[best_move[1][0]]}"
            best_txt = font_letnum.render(f"Melhor jogada: {notation} ({nome_peca})", True, (0,0,255))
            self.screen.blit(best_txt, (640//2 - best_txt.get_width()//2, 0))
            instr_txt = font_letnum.render(f"Mova o {nome_peca} de {casa_origem} para {casa_destino}", True, (200,0,0))
            self.screen.blit(instr_txt, (640//2 - instr_txt.get_width()//2, 22))
            # Destaca a peça sugerida
            pygame.draw.rect(self.screen, (255, 215, 0), (best_move[0][1]*80, best_move[0][0]*80, 80, 80), 5)
            # Destaca a casa de destino
            pygame.draw.rect(self.screen, (30, 144, 255), (best_move[1][1]*80, best_move[1][0]*80, 80, 80), 5)
        # Alerta de xeque
        if self.check_alert:
            alert_text = ChessGame.check_alert_font.render('XEQUE!', True, (255,0,0))
            self.screen.blit(alert_text, (320 - alert_text.get_width()//2, 30))
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

class TrainingChessGame(ChessGame):
    def __init__(self, screen, ai_depth):
        super().__init__(screen, ai_depth)
        self.suggestion_font = pygame.font.SysFont(None, 28)
        self.suggestions = []

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.update_suggestions()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // 80, x // 80
                    if col > 7:
                        continue  # Ignore clicks outside the board
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

    def make_move(self, start, end):
        super().make_move(start, end)
        # No AI move, just alternate turn

    def update_suggestions(self):
        from ai import get_all_moves, evaluate
        moves = get_all_moves(self.board, self.turn)
        scored = []
        for move in moves:
            new_board = copy.deepcopy(self.board)
            TrainingChessGame.apply_move_static(new_board, move)
            score = evaluate(new_board)
            scored.append((score, move))
        # Ordena as melhores jogadas para o lado que joga
        reverse = self.turn == 'w'
        scored.sort(reverse=reverse, key=lambda x: x[0])
        self.suggestions = scored[:5]

    @staticmethod
    def apply_move_static(board, move):
        start, end = move
        board[end[0]][end[1]] = board[start[0]][start[1]]
        board[start[0]][start[1]] = None

    def draw(self):
        colors = [(240,217,181), (181,136,99)]
        files = 'abcdefgh'
        ranks = '87654321'
        # Tabuleiro
        for row in range(8):
            for col in range(8):
                color = colors[(row+col)%2]
                pygame.draw.rect(self.screen, color, (col*80, row*80, 80, 80))
                if self.selected and (row, col) in self.valid_moves:
                    pygame.draw.rect(self.screen, (0,255,0), (col*80, row*80, 80, 80), 3)
                piece = self.board[row][col]
                if piece:
                    self.screen.blit(self.images[piece], (col*80, row*80))
        # Letras (a-h) abaixo
        font_letnum = pygame.font.SysFont(None, 24)
        for i in range(8):
            let = font_letnum.render(files[i], True, (0,0,0))
            self.screen.blit(let, (i*80 + 40 - let.get_width()//2, 640-20))
        # Números (1-8) à esquerda
        for i in range(8):
            num = font_letnum.render(ranks[i], True, (0,0,0))
            self.screen.blit(num, (5, i*80 + 40 - num.get_height()//2))
        # Sugestões
        pygame.draw.rect(self.screen, (220,220,220), (640, 0, 200, 640))
        title = self.suggestion_font.render('Melhores jogadas:', True, (0,0,0))
        self.screen.blit(title, (650, 20))
        from pgn import move_to_pgn
        for idx, (score, move) in enumerate(self.suggestions):
            piece = self.board[move[0][0]][move[0][1]]
            notation = move_to_pgn(piece, move[0], move[1], capture=self.board[move[1][0]][move[1][1]] is not None)
            piece_names = {'P': 'Peão', 'N': 'Cavalo', 'B': 'Bispo', 'R': 'Torre', 'Q': 'Rainha', 'K': 'Rei'}
            nome_peca = piece_names.get(piece[1], piece[1])
            pos_letras = 'abcdefgh'
            pos_numeros = '87654321'
            casa_origem = f"{pos_letras[move[0][1]]}{pos_numeros[move[0][0]]}"
            casa_destino = f"{pos_letras[move[1][1]]}{pos_numeros[move[1][0]]}"
            txt = self.suggestion_font.render(f"{notation} ({nome_peca}): {casa_origem} → {casa_destino}", True, (0,0,0))
            self.screen.blit(txt, (650, 60 + idx*30))
        # Melhor jogada destacada
        best_move, best_score = self.get_best_move()
        if best_move:
            piece = self.board[best_move[0][0]][best_move[0][1]]
            notation = move_to_pgn(piece, best_move[0], best_move[1], capture=self.board[best_move[1][0]][best_move[1][1]] is not None)
            piece_names = {'P': 'Peão', 'N': 'Cavalo', 'B': 'Bispo', 'R': 'Torre', 'Q': 'Rainha', 'K': 'Rei'}
            nome_peca = piece_names.get(piece[1], piece[1])
            pos_letras = 'abcdefgh'
            pos_numeros = '87654321'
            casa_origem = f"{pos_letras[best_move[0][1]]}{pos_numeros[best_move[0][0]]}"
            casa_destino = f"{pos_letras[best_move[1][1]]}{pos_numeros[best_move[1][0]]}"
            best_txt = font_letnum.render(f"Melhor jogada: {notation} ({nome_peca})", True, (0,0,255))
            self.screen.blit(best_txt, (650, 40))
            instr_txt = font_letnum.render(f"Mova o {nome_peca} de {casa_origem} para {casa_destino}", True, (200,0,0))
            self.screen.blit(instr_txt, (650, 60 + 5*30))
            # Destaca a peça sugerida
            pygame.draw.rect(self.screen, (255, 215, 0), (best_move[0][1]*80, best_move[0][0]*80, 80, 80), 5)
            # Destaca a casa de destino
            pygame.draw.rect(self.screen, (30, 144, 255), (best_move[1][1]*80, best_move[1][0]*80, 80, 80), 5)
        # Alerta de xeque
        if self.check_alert:
            alert_text = ChessGame.check_alert_font.render('XEQUE!', True, (255,0,0))
            self.screen.blit(alert_text, (320 - alert_text.get_width()//2, 30))
        pygame.display.flip()
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
