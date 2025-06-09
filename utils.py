import pygame
import os

def load_images():
    pieces = ['P','R','N','B','Q','K']
    colors = ['w','b']
    images = {}
    for color in colors:
        for piece in pieces:
            name = color + piece
            path = f"assets/pieces/{name}.png"
            images[name] = pygame.transform.scale(pygame.image.load(path), (80, 80))
    return images
