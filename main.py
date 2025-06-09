import pygame
import sys
from game import ChessGame
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
    quit_game = small_font.render("3. Sair", True, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(play, (WIDTH // 2 - play.get_width() // 2, 250))
    screen.blit(diff, (WIDTH // 2 - diff.get_width() // 2, 300))
    screen.blit(quit_game, (WIDTH // 2 - quit_game.get_width() // 2, 350))
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
                    return difficulty
                elif event.key == pygame.K_2:
                    index = (index + 1) % len(difficulties)
                    difficulty = difficulties[index]
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

# Iniciar menu
difficulty = menu_loop()

# Iniciar jogo
game = ChessGame(screen, DIFFICULTY_LEVELS[difficulty])
game.run()
save_pgn(game.pgn_moves)
