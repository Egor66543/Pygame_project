import pygame
import sqlite3
import random
import os
import sys

pygame.init()
pygame.font.init()


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


def terminate():
    pygame.quit()
    sys.exit()


def level_screen():
    screen = pygame.display.set_mode((800, 400))
    img1 = load_image('data/level_1.bmp')
    img2 = load_image('data/level_2.bmp')
    img3 = load_image('data/level_3.bmp')
    # img4 = load_image('data/бонусный уровень')
    screen.blit(img1, (50, 150))
    screen.blit(img2, (250, 150))
    screen.blit(img3, (450, 150))
    # screen.blit(img3, (650, 150)
    font = pygame.font.Font(None, 40)
    text = font.render('ВЫБЕРИТЬ УРОВЕНЬ', True, 'white')
    screen.blit(text, (260, 20))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and (50 <= x <= 240 and 150 <= y <= 250):
                return (1, 10)
            elif event.type == pygame.MOUSEBUTTONDOWN and (250 <= x <= 440 and 150 <= y <= 250):
                return (11, 20)
            elif event.type == pygame.MOUSEBUTTONDOWN and (450 <= x <= 640 and 150 <= y <= 250):
                return (21, 30)
        pygame.display.flip()


a, b = level_screen()
con = sqlite3.connect("game_words.db")
cur = con.cursor()
while True:
    id_word = cur.execute(f'''select id from words where id={random.randint(a, b)}''').fetchone()[0]
    characteristic = cur.execute(f'''select characteristic from words where id={id_word}''').fetchone()[0]
    if characteristic == '-':
        break
word = cur.execute(f'''SELECT word FROM words WHERE id={id_word}''').fetchone()[0]
description = cur.execute(f'''SELECT description FROM words WHERE id={id_word}''').fetchone()[0]
level = cur.execute(f'''SELECT level FROM words WHERE id={id_word}''').fetchone()[0]


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

text_ = ''


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(text_, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        global text_
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    text_ = text_[:-1]  # Wrong work!!!!
                else:
                    text_ += event.unicode
                self.render_text()


def letter_in_word():
    letter = text_[-1]
    h, c = 0, 0
    if letter in word:
        sp = [i for i, j in enumerate(word) if j == letter]
        font = pygame.font.Font(None, 50)
        for i in range(len(sp)):
            text = font.render(f'{letter}', True, 'white')
            board.screen.blit(text, (60 + 50 * sp[i], 400))
    elif letter not in word:
        pass


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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            letter_in_word()
    all_lamp_sprites.draw(board.screen)
    grop_1.update(event_list)

    grop_1.draw(board.screen)
    pygame.display.flip()

pygame.quit()
