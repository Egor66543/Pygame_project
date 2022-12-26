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
level = cur.execute(f'''SELECT level FROM words WHERE id={id_word}''').fetchone()[0]


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


def description_f():
    h = 0
    font2 = pygame.font.Font(None, 24)
    strings = description.split('?')
    for i in range(len(strings)):
        text = font2.render(strings[i].replace('\n', ''), True, 'white')
        board.screen.blit(text, (50, 500 + h))
        h += 15


class Board:
    def __init__(self, h, w):
        self.h, self.w = h, w
        self.screen = pygame.display.set_mode((h, w))
        self.a = 50
        self.point = 0

    def render(self):
        font1 = pygame.font.Font(None, 20)
        text = font1.render(f'Points: {self.point}', True, 'white')
        board.screen.blit(text, (60, 10))

        text = font1.render(f'Level: {level}', True, 'white')
        board.screen.blit(text, (130, 10))

        k = 0
        for _ in range(len(word)):
            pygame.draw.rect(self.screen, 'white', (50 + k, 400, self.a, self.a), 2)
            k += self.a


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()


board = Board(800, 700)
board.render()

all_lamp_sprites = pygame.sprite.Group()
lamp = pygame.sprite.Sprite(all_lamp_sprites)
lamp.image = load_image("data/lamp.jpg")
lamp.rect = lamp.image.get_rect()
lamp.mask = pygame.mask.from_surface(lamp.image)

font = pygame.font.Font(None, 20)
text1 = font.render('Введите букву:', True, 'white')
board.screen.blit(text1, (405, 10))

field_for_entering_letters = pygame.draw.rect(board.screen, 'white', (400, 5, 395, 300), 2)
font_letter = pygame.font.Font(None, 100)
text_input_box = TextInputBox(400, 30, 395, font_letter)
grop_1 = pygame.sprite.Group(text_input_box)
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and (0 <= x <= 50 and 0 <= y <= 51):
            description_f()
    all_lamp_sprites.draw(board.screen)
    grop_1.update(event_list)
    grop_1.draw(board.screen)
    pygame.display.flip()

pygame.quit()
