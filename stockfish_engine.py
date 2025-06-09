import chess
import chess.engine

STOCKFISH_PATH = r"C:\Users\Israel Neto\Desktop\chess\stockfish\stockfish-windows-x86-64-avx2.exe"  # Altere para o seu caminho

def stockfish_move(fen: str, time_limit=0.2) -> str:
    board = chess.Board(fen)
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    result = engine.play(board, chess.engine.Limit(time=time_limit))
    engine.quit()
    return result.move.uci()
