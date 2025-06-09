def pos_to_alg(pos):
    files = 'abcdefgh'
    ranks = '87654321'
    return files[pos[1]] + ranks[pos[0]]

def move_to_pgn(piece, start, end, capture=False, promotion=None, castle=None):
    if castle: return castle
    piece_letter = '' if piece[1] == 'P' else piece[1]
    end_sq = pos_to_alg(end)
    capture_sign = 'x' if capture else ''
    promo = f'={promotion}' if promotion else ''
    return f"{piece_letter}{capture_sign}{end_sq}{promo}"

def save_pgn(moves, filename='partida.pgn'):
    with open(filename, 'w') as f:
        f.write('[Event "Partida com IA"]\n')
        f.write('[Site "Local"]\n')
        f.write('[Date "2025.06.09"]\n')
        f.write('[Round "-"]\n')
        f.write('[White "Jogador"]\n')
        f.write('[Black "IA"]\n')
        f.write('[Result "*"]\n\n')
        f.write(' '.join(moves) + '\n')
