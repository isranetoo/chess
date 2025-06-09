def board_to_fen(board, turn='w', castling='KQkq', ep='-', halfmove=0, fullmove=1):
    # Converte o tabuleiro (matriz) para FEN (apenas posição, sem roque/EP precisos)
    fen_rows = []
    for row in board:
        empty = 0
        fen_row = ''
        for piece in row:
            if not piece:
                empty += 1
            else:
                if empty:
                    fen_row += str(empty)
                    empty = 0
                letter = piece[1]
                if piece[0] == 'w':
                    fen_row += letter.upper()
                else:
                    fen_row += letter.lower()
        if empty:
            fen_row += str(empty)
        fen_rows.append(fen_row)
    fen = '/'.join(fen_rows)
    return f"{fen} {turn} {castling} {ep} {halfmove} {fullmove}"

def get_stockfish_best_move(board, turn, stockfish_path, time_limit=0.2):
    from stockfish_engine import stockfish_move
    fen = board_to_fen(board, turn)
    return stockfish_move(fen, time_limit=time_limit)

import copy
from chess_rules import get_piece_moves

DIFFICULTY_LEVELS = {
    'Fácil': 1,
    'Médio': 2,
    'Difícil': 3
}

def minimax(board, depth, is_maximizing):
    if depth == 0:
        return evaluate(board), None

    best_move = None
    if is_maximizing:
        max_eval = float('-inf')
        for move in get_all_moves(board, 'w'):
            new_board = copy.deepcopy(board)
            apply_move(new_board, move)
            eval, _ = minimax(new_board, depth-1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in get_all_moves(board, 'b'):
            new_board = copy.deepcopy(board)
            apply_move(new_board, move)
            eval, _ = minimax(new_board, depth-1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

def get_all_moves(board, color):
    # Usa movimentos reais de xadrez
    moves = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == color:
                for move in get_piece_moves(board, r, c):
                    moves.append(((r, c), move))
    return moves

def apply_move(board, move):
    start, end = move
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = None

def evaluate(board):
    piece_values = {'P': 1, 'N': 3.2, 'B': 3.3, 'R': 5.1, 'Q': 9.5, 'K': 0}
    value = 0
    mobility = 0
    center_bonus = 0
    king_safety = 0
    center_squares = [(3,3),(3,4),(4,3),(4,4)]
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece:
                sign = 1 if piece[0] == 'w' else -1
                # Valor material
                value += sign * piece_values[piece[1]]
                # Bônus por controle do centro
                if (r, c) in center_squares:
                    center_bonus += sign * 0.2
                # Segurança do rei (penaliza rei exposto)
                if piece[1] == 'K':
                    if (piece[0] == 'w' and r < 2) or (piece[0] == 'b' and r > 5):
                        king_safety += sign * 0.3
    # Mobilidade (número de jogadas possíveis)
    from chess_rules import get_piece_moves
    for color in ['w', 'b']:
        moves = 0
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece[0] == color:
                    moves += len(get_piece_moves(board, r, c))
        if color == 'w':
            mobility += 0.05 * moves
        else:
            mobility -= 0.05 * moves
    return value + center_bonus + mobility + king_safety
