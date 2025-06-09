import copy

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
    # Simples: pega todas as peças e retorna movimentos para qualquer casa livre
    moves = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == color:
                for r2 in range(8):
                    for c2 in range(8):
                        if board[r2][c2] is None or board[r2][c2][0] != color:
                            moves.append(((r, c), (r2, c2)))
    return moves

def apply_move(board, move):
    start, end = move
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = None

def evaluate(board):
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
    value = 0
    for row in board:
        for piece in row:
            if piece:
                sign = 1 if piece[0] == 'w' else -1
                value += sign * piece_values[piece[1]]
    return value
