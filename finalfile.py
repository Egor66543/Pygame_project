import pygame
import sqlite3
import random
import os
import sys

pygame.init()
pygame.font.init()
STATE = 0


def selection_screen():
    screen = pygame.display.set_mode((800, 400))
    pygame.draw.rect(screen, 'MediumAquamarine', (50, 130, 300, 80), 1)
    pygame.draw.rect(screen, 'MediumAquamarine', (450, 130, 300, 80), 1)
    font = pygame.font.Font(None, 50)
    text1 = font.render('ИГРА 1', True, 'MediumAquamarine')
    text2 = font.render('ИГРА 2', True, 'MediumAquamarine')
    text3 = font.render('ВЫБЕРИТЕ ИГРУ', True, 'LightSeaGreen')
    screen.blit(text1, (140, 160))
    screen.blit(text2, (540, 160))
    screen.blit(text3, (250, 10))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and (50 <= x <= 350 and 130 <= y <= 220):
                return 1
            elif event.type == pygame.MOUSEBUTTONDOWN and (450 <= x <= 750 and 130 <= y <= 220):
                return 2
        pygame.display.flip()


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


def rules_screen():
    screen = pygame.display.set_mode((800, 400))
    with open('rules', encoding='utf-8') as file:
        h = 0
        f = file.read().split('\n')
        for i in range(len(f)):
            font = pygame.font.Font(None, 20)
            text = font.render(f[i], True, 'white')
            screen.blit(text, (0, 0 + h))
            h += 20
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return level_screen()
        pygame.display.flip()


def level_screen():
    screen = pygame.display.set_mode((800, 400))
    img1 = load_image('data/level_1.bmp')
    img2 = load_image('data/level_2.bmp')
    img3 = load_image('data/level_3.bmp')
    img4 = load_image('data/bonus.png')
    infoimg = load_image('data/info.png')
    screen.blit(img1, (50, 150))
    screen.blit(img2, (250, 150))
    screen.blit(img3, (450, 150))
    screen.blit(img4, (630, 150))
    screen.blit(infoimg, (730, 330))
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
            elif event.type == pygame.MOUSEBUTTONDOWN and (450 <= x <= 600 and 150 <= y <= 250):
                return (21, 30)
            elif event.type == pygame.MOUSEBUTTONDOWN and (620 <= x <= 750 and 150 <= y <= 250):
                return (31, 31)
            elif event.type == pygame.MOUSEBUTTONDOWN and (730 <= x <= 800 and 330 <= y <= 400):
                return rules_screen()
        pygame.display.flip()


def game_over_screen():
    screen = pygame.display.set_mode((600, 400))
    img = load_image('data/gameover.png')
    screen.blit(img, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return selection_screen()
        pygame.display.flip()


def winner_screen():
    screen = pygame.display.set_mode((900, 600))
    img = load_image('data/winners-image.jpg')
    screen.blit(img, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return selection_screen()
        pygame.display.flip()


def water():
    if c == 2:
        pygame.draw.rect(board.screen, 'black', (62, 100, 238, 50))
    elif c == 3:
        pygame.draw.rect(board.screen, 'black', (62, 100, 238, 150))
    pygame.display.flip()


def description_f():
    h = 0
    font2 = pygame.font.Font(None, 24)
    strings = description.split('?')
    for i in range(len(strings)):
        text = font2.render(strings[i].replace('\n', ''), True, 'white')
        board.screen.blit(text, (50, 500 + h))
        h += 15


def draw_text(text_x, text_y, size, message_text):
    global screen
    font = pygame.font.Font(None, size)
    text = font.render(message_text, True, (255, 255, 255))
    screen.blit(text, (text_x, text_y))


def render():
    global points
    screen.fill((0, 0, 0))
    image = load_image('fon.jpg')
    screen.blit(image, (0, 0))
    image = load_image('skip_question_button.png')
    screen.blit(image, (0, 480))
    image = load_image('exit_button.png')
    screen.blit(image, (578, 480))
    if suggest:
        image = load_image('50_50.png')
        screen.blit(image, (60, 480))
    if hall:
        image = load_image('hall_help.jpg')
        screen.blit(image, (140, 480))

    draw_text(60, 90, 30, f[question_number])
    if answers[0]:
        draw_text(130, 210, 30, f[question_number + 1])
    if answers[1]:
        draw_text(130, 280, 30, f[question_number + 2])
    if answers[2]:
        draw_text(130, 350, 30, f[question_number + 3])
    if answers[3]:
        draw_text(130, 420, 30, f[question_number + 4])
    if suggest_hall:
        if answers[0]:
            draw_text(540, 210, 30, hall_help_list[0])
        if answers[1]:
            draw_text(540, 280, 30, hall_help_list[1])
        if answers[2]:
            draw_text(540, 350, 30, hall_help_list[2])
        if answers[3]:
            draw_text(540, 420, 30, hall_help_list[3])

    draw_text(470, 500, 30, f"points {str(points)}")
    draw_text(360, 500, 30, f"Время {str(int(timer))}")


def render_menu():
    image = load_image('level_button.png')
    screen.blit(image, (15, 40))
    image = load_image('level_button.png')
    screen.blit(image, (15, 110))
    image = load_image('level_button.png')
    screen.blit(image, (15, 410))
    image = load_image('1.svg')
    screen.blit(image, (300, 20))
    draw_text(70, 60, 30, "Level 1")
    draw_text(70, 130, 30, "Level 2")
    draw_text(70, 430, 30, "Выход")


def checking_the_answer():
    global points, question_number, user_answer, running, end_game, answers
    if user_answer == int(f[question_number + 5]):
        play_music("data/music_right_answer.mp3")
        points += 1
    else:
        play_music("data/music_wrong_answer.mp3")
    user_answer = 0
    next_question()


def suggest_50_50():
    global suggest, question_number, answers
    play_music('data/50_50_music.mp3')
    suggest = False
    while True:
        false_answer = random.choice([1, 2, 3, 4])
        if false_answer != int(f[question_number + 5]):
            answers = [0, 0, 0, 0]
            answers[false_answer - 1] = 1
            answers[int(f[question_number + 5]) - 1] = 1
            break


def hall_help():
    global hall, hall_help_list, suggest_hall
    play_music('data/hall_help.mp3')
    hall = False
    suggest_hall = True
    random.shuffle(hall_help_list)


def next_question():
    global question_number, running, end_game, answers, timer, suggest_hall
    answers = [1, 1, 1, 1]
    suggest_hall = False
    timer = timer_game
    question_number += 6
    if question_number == 120 or question_number == 240:
        running = False
        end_game = True
        start_screen()


def time_out():
    global timer
    play_music('data/time-out.mp3')
    timer = timer_game
    next_question()


def music_player():
    global flPause, vol, event
    if event.key == pygame.K_SPACE:
        flPause = not flPause
        if flPause:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    elif event.key == pygame.K_LEFT:
        vol -= 0.1
        pygame.mixer.music.set_volume(vol)
    elif event.key == pygame.K_RIGHT:
        vol += 0.1
        pygame.mixer.music.set_volume(vol)


def play_music(name_music):
    pygame.mixer.music.load(name_music)
    pygame.mixer.music.play()


def start_screen():
    global event
    if end_game:
        play_music('data/end_game.mp3')
        intro_text = ["Игра окончена", "",
                      f"Вы набрали {points} баллов"]
    else:
        intro_text = ["Викторина", "",
                      "1 правильный ответ",
                      "приносит 1 балл",
                      "Всего в викторине 40 вопросов"]
    fon = pygame.transform.scale(load_image('start_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if end_game:
                    menu()
                return
        pygame.display.flip()


def level(difficulty_level):
    global running, timer, timer_game, suggest, question_number, hall
    play_music('data/music_first_question.mp3')
    running = True
    if difficulty_level == 1:
        timer_game = 31
        timer = 32
        suggest = True
        hall = True
        question_number = 0
    elif difficulty_level == 2:
        timer_game = 21
        timer = 22
        suggest = False
        hall = False
        question_number = 120


def menu():
    global running, f, event, x, y, answers, suggest_hall
    answers = [1, 1, 1, 1]
    suggest_hall = False
    play_music("data/start_menu_music.mp3")
    f = open('data/question', encoding='utf-8', mode='r+')
    f = f.read().split('\n')
    screen.fill((0, 0, 0))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and (15 <= x <= 195 and 40 <= y <= 100):
                level(1)
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and (15 <= x <= 195 and 110 <= y <= 170):
                level(2)
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and (15 <= x <= 195 and 410 <= y <= 470):
                terminate()
            elif event.type == pygame.KEYDOWN:
                music_player()
        pygame.mixer.music.queue("data/menu_music.mp3")
        render_menu()
        pygame.display.flip()


class Board:
    def __init__(self, h, w):
        self.h, self.w = h, w
        self.screen = pygame.display.set_mode((h, w))
        self.a = 50

    def render(self):
        self.screen.fill(0)
        font1 = pygame.font.Font(None, 20)
        text = font1.render(f'Points: {point}', True, 'white')
        board.screen.blit(text, (60, 10))

        text = font1.render(f'Level: {level}', True, 'white')
        board.screen.blit(text, (170, 10))

        pygame.draw.line(board.screen, 'white', (60, 80), (60, 300), width=2)
        pygame.draw.line(board.screen, 'white', (300, 80), (300, 300), width=2)
        pygame.draw.line(board.screen, 'white', (60, 300), (300, 300), width=2)
        pygame.draw.rect(board.screen, 'Navy', (62, 100, 238, 200))

        k = 0
        for _ in range(len(word)):
            pygame.draw.rect(self.screen, 'white', (50 + k, 400, self.a, self.a), 2)
            k += self.a

    def update_points(self):
        pygame.draw.rect(self.screen, 'black', (55, 0, 100, 30))
        font1 = pygame.font.Font(None, 20)
        text = font1.render(f'Points: {point}', True, 'white')
        board.screen.blit(text, (60, 10))


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
                    text_ = text_[:-1]
                else:
                    text_ += event.unicode
                self.render_text()


c = 1


def letter_in_word():
    global point
    global c
    global dl
    letter = text_[-1]
    h = 0
    if c == 3:
        game_over_screen()
    else:
        if letter in word:
            sp = [i for i, j in enumerate(word) if j == letter]
            for i in range(len(sp)):
                font1 = pygame.font.Font(None, 50)
                text = font1.render(f'{letter}', True, 'white')
                board.screen.blit(text, (60 + 50 * sp[i], 400))
            dl -= 1 * len(sp)
        elif letter not in word:
            c += 1
            point -= FINE[level]
            board.update_points()
            h += 20
    if dl <= 0:
        point += W_POINTS[level]
        board.update_points()
        cur.execute(f'''update words set characteristic = "+" where id={id_word}''')
        con.commit()
        winner_screen()
    water()


STATE = selection_screen()
if STATE == 2:
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
    point = 0
    dl = len(word)
    FINE = {1: 10, 2: 30, 3: 40, 'bonus': 100}
    W_POINTS = {1: 50, 2: 150, 3: 250, 'bonus': 1000}

    board = Board(800, 700)
    board.render()

    all_lamp_sprites = pygame.sprite.Group()
    lamp = pygame.sprite.Sprite(all_lamp_sprites)
    lamp.image = load_image("data/lamp.jpg")
    lamp.rect = lamp.image.get_rect()

    font = pygame.font.Font(None, 20)
    text1 = font.render('Введите букву:', True, 'white')
    board.screen.blit(text1, (405, 10))

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
                point -= 100
                board.update_points()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                letter_in_word()
        all_lamp_sprites.draw(board.screen)
        grop_1.update(event_list)
        grop_1.draw(board.screen)
        pygame.display.flip()

    pygame.quit()

elif STATE == 1:
    pygame.init()
    points = 0
    question_number = 0
    user_answer = 0
    all_sprites = pygame.sprite.Group()
    width = 638
    height = 539
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    end_game = False
    suggest = True
    hall = True
    FPS = 50
    answers = [1, 1, 1, 1]
    vol = 1.0
    flPause = False
    running = False
    timer = 0
    timer_game = 0
    f = []
    hall_help_list = ['40%', '30%', '20%', '10%']
    suggest_hall = False

    start_screen()
    menu()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and (100 <= x <= 570 and 190 <= y <= 450):
                user_answer = (y - 190) // 65 + 1
            elif suggest and event.type == pygame.MOUSEBUTTONDOWN and (61 <= x <= 140 and 480 <= y <= 540):
                suggest_50_50()
            elif hall and event.type == pygame.MOUSEBUTTONDOWN and (141 <= x <= 220 and 480 <= y <= 540):
                hall_help()
            elif event.type == pygame.MOUSEBUTTONDOWN and (0 <= x <= 60 and 480 <= y <= 540):
                next_question()
            elif event.type == pygame.MOUSEBUTTONDOWN and (578 <= x <= 638 and 480 <= y <= 540):
                running = False
                menu()
            elif event.type == pygame.KEYDOWN:
                music_player()
        timer -= clock.tick(1000) / 1000
        if int(timer) == 0:
            time_out()
        if user_answer != 0:
            checking_the_answer()
        pygame.mixer.music.queue("data/fon_music.mp3")
        render()
        pygame.display.flip()

terminate()
