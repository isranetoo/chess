import pygame
import sys
from game import ChessGame, TrainingChessGame
from ai import DIFFICULTY_LEVELS
from pgn import save_pgn

pygame.init()
WIDTH, HEIGHT = 640, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Xadrez com IA")
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

difficulty = 'Médio'

def draw_menu(selected_difficulty):
    screen.fill((240, 217, 181))
    title = font.render("Xadrez", True, (0, 0, 0))
    play = small_font.render("1. Jogar", True, (0, 0, 0))
    diff = small_font.render(f"2. Dificuldade: {selected_difficulty}", True, (0, 0, 0))
    treino = small_font.render("3. Modo Treino", True, (0, 0, 0))
    stockfish = small_font.render("4. Modo Stockfish", True, (0, 0, 0))
    quit_game = small_font.render("5. Sair", True, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(play, (WIDTH // 2 - play.get_width() // 2, 250))
    screen.blit(diff, (WIDTH // 2 - diff.get_width() // 2, 300))
    screen.blit(treino, (WIDTH // 2 - treino.get_width() // 2, 350))
    screen.blit(stockfish, (WIDTH // 2 - stockfish.get_width() // 2, 400))
    screen.blit(quit_game, (WIDTH // 2 - quit_game.get_width() // 2, 450))
    pygame.display.flip()

def menu_loop():
    global difficulty
    difficulties = list(DIFFICULTY_LEVELS.keys())
    index = difficulties.index(difficulty)
    while True:
        draw_menu(difficulty)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'normal', difficulty, 'w'
                elif event.key == pygame.K_2:
                    index = (index + 1) % len(difficulties)
                    difficulty = difficulties[index]
                elif event.key == pygame.K_3:
                    # Escolher cor para treino
                    color = choose_color()
                    return 'treino', difficulty, color
                elif event.key == pygame.K_4:
                    # Escolher cor para stockfish
                    color = choose_color()
                    return 'stockfish', difficulty, color
                elif event.key == pygame.K_5:
                    pygame.quit()
                    sys.exit()

def choose_color():
    # Tela simples para escolher cor
    while True:
        screen.fill((240, 217, 181))
        font_big = pygame.font.SysFont(None, 48)
        txt = font_big.render('Escolha sua cor:', True, (0,0,0))
        wtxt = font_big.render('1. Brancas', True, (0,0,0))
        btxt = font_big.render('2. Pretas', True, (0,0,0))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 200))
        screen.blit(wtxt, (WIDTH//2 - wtxt.get_width()//2, 300))
        screen.blit(btxt, (WIDTH//2 - btxt.get_width()//2, 370))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'w'
                elif event.key == pygame.K_2:
                    return 'b'


modo, difficulty, user_color = menu_loop()

if modo == 'normal':
    game_normal = ChessGame(screen, DIFFICULTY_LEVELS[difficulty])
    game_normal.run()
    save_pgn(game_normal.pgn_moves)
elif modo == 'treino':
    screen_treino = pygame.display.set_mode((840, 640))
    game_treino = TrainingChessGame(screen_treino, DIFFICULTY_LEVELS[difficulty])
    # Passa a cor escolhida para o modo treino
    game_treino.user_color = user_color
    # Sempre brancas começam
    game_treino.turn = 'w'
    game_treino.selected = None
    game_treino.valid_moves = []
    game_treino.game_over = False
    game_treino.pgn_moves = []
    game_treino.move_number = 1
    if user_color == 'b':
        # Faz a IA jogar primeiro
        from ai import minimax
        _, move = minimax(game_treino.board, DIFFICULTY_LEVELS[difficulty], False)
        if move:
            game_treino.make_move(*move)
    game_treino.run()
elif modo == 'stockfish':
    import chess
    from stockfish_engine import stockfish_move
    import time
    board = chess.Board()
    selected = None
    last_fen = None
    stockfish_suggestion = None
    running = True
    # Sempre brancas começam
    board.turn = chess.WHITE
    # Não faz nenhum movimento automático, independente da cor escolhida
    selected = None
    while running:
        screen.fill((240, 217, 181))
        # Desenha o tabuleiro (ajusta orientação conforme cor do usuário)
        # O tabuleiro do python-chess é indexado por [rank][file] (0,0) = a8 (canto superior esquerdo)
        # Para garantir que a cor escolhida fique embaixo:
        if user_color == 'w':
            # Brancas embaixo: desenhar de rank 7 a 0 (de baixo para cima)
            for display_row, board_row in enumerate(range(7, -1, -1)):
                for col in range(8):
                    color = (240,217,181) if ((board_row+col)%2==0) else (181,136,99)
                    pygame.draw.rect(screen, color, (col*80, display_row*80, 80, 80))
                    piece = board.piece_at(board_row*8+col)
                    if piece:
                        img = pygame.image.load(f"assets/pieces/{'w' if piece.color else 'b'}{piece.symbol().upper()}.png")
                        img = pygame.transform.scale(img, (80, 80))
                        screen.blit(img, (col*80, display_row*80))
        else:
            # Pretas embaixo: desenhar de rank 0 a 7 (de baixo para cima)
            for display_row, board_row in enumerate(range(0, 8)):
                for display_col, board_col in enumerate(range(7, -1, -1)):
                    color = (240,217,181) if ((board_row+board_col)%2==0) else (181,136,99)
                    pygame.draw.rect(screen, color, (display_col*80, display_row*80, 80, 80))
                    piece = board.piece_at(board_row*8+board_col)
                    if piece:
                        img = pygame.image.load(f"assets/pieces/{'w' if piece.color else 'b'}{piece.symbol().upper()}.png")
                        img = pygame.transform.scale(img, (80, 80))
                        screen.blit(img, (display_col*80, display_row*80))
        # Letras e números (ajustados para orientação)
        font_letnum = pygame.font.SysFont(None, 24)
        files = 'abcdefgh'
        ranks = '87654321'
        if user_color == 'w':
            # Brancas embaixo
            for i in range(8):
                let = font_letnum.render(files[i], True, (0,0,0))
                screen.blit(let, (i*80 + 40 - let.get_width()//2, 640-20))
            for i in range(8):
                num = font_letnum.render(ranks[7-i], True, (0,0,0))
                screen.blit(num, (5, i*80 + 40 - num.get_height()//2))
        else:
            # Pretas embaixo
            for i in range(8):
                let = font_letnum.render(files[7-i], True, (0,0,0))
                screen.blit(let, (i*80 + 40 - let.get_width()//2, 640-20))
            for i in range(8):
                num = font_letnum.render(ranks[i], True, (0,0,0))
                screen.blit(num, (5, i*80 + 40 - num.get_height()//2))
        # Lateral para sugestão e possibilidades
        pygame.draw.rect(screen, (220,220,220), (640, 0, 200, 640))
        title = font_letnum.render('Sugestão Stockfish:', True, (0,0,0))
        screen.blit(title, (650, 20))
        stockfish_path = r"C:/Users/Israel Neto/Desktop/chess/stockfish/stockfish-windows-x86-64-avx2.exe"
        # Só chama o Stockfish se o tabuleiro mudou
        if not board.is_game_over():
            if last_fen != board.fen():
                move = stockfish_move(board.fen(), time_limit=0.3)
                stockfish_suggestion = move
                last_fen = board.fen()
            move = stockfish_suggestion
            move_str = str(move) if move else ''
            piece_names = {'p': 'Peão', 'n': 'Cavalo', 'b': 'Bispo', 'r': 'Torre', 'q': 'Rainha', 'k': 'Rei'}
            if move is not None:
                from_square = chess.parse_square(move_str[:2])
                to_square = chess.parse_square(move_str[2:4])
                piece = board.piece_at(from_square)
                nome_peca = piece_names.get(piece.symbol().lower(), piece.symbol()) if piece else ''
                # Ajusta destaque conforme orientação
                if user_color == 'w':
                    draw_from_file = chess.square_file(from_square)
                    draw_from_rank = 7 - chess.square_rank(from_square)
                    draw_to_file = chess.square_file(to_square)
                    draw_to_rank = 7 - chess.square_rank(to_square)
                else:
                    draw_from_file = 7 - chess.square_file(from_square)
                    draw_from_rank = chess.square_rank(from_square)
                    draw_to_file = 7 - chess.square_file(to_square)
                    draw_to_rank = chess.square_rank(to_square)
                # Destaca a peça sugerida
                pygame.draw.rect(screen, (255, 215, 0), (draw_from_file*80, draw_from_rank*80, 80, 80), 5)
                # Destaca a casa de destino
                pygame.draw.rect(screen, (30, 144, 255), (draw_to_file*80, draw_to_rank*80, 80, 80), 5)
                best_txt = font_letnum.render(f"{move_str} ({nome_peca})", True, (0,0,255))
                screen.blit(best_txt, (650, 60))
                instr_txt = font_letnum.render(f"Mova o {nome_peca} de {move_str[:2]} para {move_str[2:4]}", True, (200,0,0))
                screen.blit(instr_txt, (650, 100))
            else:
                best_txt = font_letnum.render("Stockfish não sugeriu jogada", True, (200,0,0))
                screen.blit(best_txt, (650, 60))
        else:
            result_txt = font_letnum.render("Fim de jogo!", True, (200,0,0))
            screen.blit(result_txt, (650, 60))

        # Mostra as possibilidades da peça selecionada
        if selected is not None and board.piece_at(selected) and board.piece_at(selected).color == board.turn:
            moves = [m for m in board.legal_moves if m.from_square == selected]
            poss_title = font_letnum.render('Possibilidades:', True, (0,0,0))
            screen.blit(poss_title, (650, 180))
            for idx, m in enumerate(moves):
                # Ajusta destino conforme orientação
                dest_file = chess.square_file(m.to_square)
                dest_rank = chess.square_rank(m.to_square)
                if user_color == 'w':
                    draw_dest_file = dest_file
                    draw_dest_rank = dest_rank
                else:
                    draw_dest_file = 7 - dest_file
                    draw_dest_rank = 7 - dest_rank
                dest_alg = chess.square_name(m.to_square)
                poss_txt = font_letnum.render(f"{dest_alg}", True, (0,128,0))
                screen.blit(poss_txt, (650, 210 + idx*25))
                # Destaca as casas possíveis
                pygame.draw.rect(screen, (0, 200, 0), (draw_dest_file*80, draw_dest_rank*80, 80, 80), 3)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not board.is_game_over():
                x, y = pygame.mouse.get_pos()
                # Ajusta o cálculo do quadrado conforme orientação
                if user_color == 'w':
                    row = 7 - (y // 80)
                    col = x // 80
                else:
                    row = y // 80
                    col = 7 - (x // 80)
                square = row * 8 + col
                if board.piece_at(square) and board.piece_at(square).color == board.turn:
                    selected = square
                else:
                    try:
                        move = chess.Move(selected, square)
                        if move in board.legal_moves:
                            board.push(move)
                            selected = None
                    except:
                        selected = None
        time.sleep(0.05)
