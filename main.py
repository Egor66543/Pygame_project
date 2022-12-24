import pygame
import sqlite3
import random
import os
import sys

pygame.init()
pygame.font.init()

con = sqlite3.connect("game_words.db")
cur = con.cursor()
id_word = cur.execute(f'''select id from words where id={random.randint(1, 10)}''').fetchone()[0]
word = cur.execute(f'''SELECT word FROM words WHERE id={id_word}''').fetchone()[0]
description = cur.execute(f'''SELECT description FROM words WHERE id={id_word}''').fetchone()[0]
res = id_word, word, description


def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        print('Файл не найден')
        sys.exit()
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image.convert_alpha()
    return image


class Board:
    def __init__(self, h, w):
        self.h, self.w = h, w
        self.screen = pygame.display.set_mode((h, w))
        self.a = 50

    def render(self):
        k = 0
        for x in range(len(res[1])):
            pygame.draw.rect(self.screen, 'white', (50 + k, 400, self.a, self.a), 1)
            k += self.a

    def description(self):
        font1 = pygame.font.Font(None, 24)
        text = font1.render(res[2], True, 'white')
        board.screen.blit(text, (50, 500))


board = Board(800, 700)
board.render()
board.render()
all_sprites = pygame.sprite.Group()
lamp = pygame.sprite.Sprite(all_sprites)
lamp.image = load_image("data/lamp.jpg")
lamp.rect = lamp.image.get_rect()
lamp.mask = pygame.mask.from_surface(lamp.image)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and (0 <= x <= 50 and 0 <= y <= 51):
            board.description()

    all_sprites.draw(board.screen)
    pygame.display.flip()

pygame.quit()





