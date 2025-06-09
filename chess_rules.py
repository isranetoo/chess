def is_in_check(board, color):
    # Encontra o rei
    king_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] == color + 'K':
                king_pos = (r, c)
                break
        if king_pos:
            break
    if not king_pos:
        return False  # Rei não encontrado (deve ser mate)
    # Verifica se alguma peça adversária pode capturar o rei
    opp_color = 'b' if color == 'w' else 'w'
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == opp_color:
                moves = get_piece_moves(board, r, c)
                if king_pos in moves:
                    return True
    return False
def is_in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def pawn_moves(board, row, col, color):
    moves = []
    direction = -1 if color == 'w' else 1
    start_row = 6 if color == 'w' else 1
    # Forward
    if is_in_bounds(row + direction, col) and board[row + direction][col] is None:
        moves.append((row + direction, col))
        # Double move from start
        if row == start_row and board[row + 2 * direction][col] is None:
            moves.append((row + 2 * direction, col))
    # Captures
    for dc in [-1, 1]:
        nr, nc = row + direction, col + dc
        if is_in_bounds(nr, nc) and board[nr][nc] and board[nr][nc][0] != color:
            moves.append((nr, nc))
    return moves

def knight_moves(board, row, col, color):
    moves = []
    for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        nr, nc = row + dr, col + dc
        if is_in_bounds(nr, nc) and (board[nr][nc] is None or board[nr][nc][0] != color):
            moves.append((nr, nc))
    return moves

def sliding_moves(board, row, col, color, directions):
    moves = []
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        while is_in_bounds(nr, nc):
            if board[nr][nc] is None:
                moves.append((nr, nc))
            elif board[nr][nc][0] != color:
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves

def bishop_moves(board, row, col, color):
    return sliding_moves(board, row, col, color, [(-1,-1),(-1,1),(1,-1),(1,1)])

def rook_moves(board, row, col, color):
    return sliding_moves(board, row, col, color, [(-1,0),(1,0),(0,-1),(0,1)])

def queen_moves(board, row, col, color):
    return bishop_moves(board, row, col, color) + rook_moves(board, row, col, color)

def king_moves(board, row, col, color):
    moves = []
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if is_in_bounds(nr, nc) and (board[nr][nc] is None or board[nr][nc][0] != color):
                moves.append((nr, nc))
    return moves

def get_piece_moves(board, row, col):
    piece = board[row][col]
    if not piece:
        return []
    color, ptype = piece[0], piece[1]
    if ptype == 'P':
        return pawn_moves(board, row, col, color)
    elif ptype == 'N':
        return knight_moves(board, row, col, color)
    elif ptype == 'B':
        return bishop_moves(board, row, col, color)
    elif ptype == 'R':
        return rook_moves(board, row, col, color)
    elif ptype == 'Q':
        return queen_moves(board, row, col, color)
    elif ptype == 'K':
        return king_moves(board, row, col, color)
    return []
