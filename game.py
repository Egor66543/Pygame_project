import os
import sys
import pygame
import random


pygame.init()
points = 0
question_number = 0
user_answer = 0
all_sprites = pygame.sprite.Group()
width = 500
height = 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
end_game = False
suggest = True
hall = True
FPS = 50
answers = [1, 1, 1, 1]
vol = 1.0
flPause = False
running = True
timer = 0
timer_game = 0
f = []
hall_help_list = ['40%', '30%', '20%', '10%']
suggest_hall = False
x, y = pygame.mouse.get_pos()
event = pygame.event.get()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((2, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_text(text_x, text_y, size, message_text):
    global screen
    font = pygame.font.Font(None, size)
    text = font.render(message_text, True, (255, 255, 255))
    screen.blit(text, (text_x, text_y))


def render_quiz():
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


def render_menu_quiz():
    image = load_image('level_button.png')
    screen.blit(image, (15, 40))
    image = load_image('level_button.png')
    screen.blit(image, (15, 110))
    image = load_image('level_button.png')
    screen.blit(image, (15, 410))
    image = load_image('logo.svg')
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
        start_screen_quiz()


def time_out():
    global timer
    play_music('data/time-out.mp3')
    timer = timer_game
    next_question()


def music_player(ev):
    global flPause, vol
    if ev.key == pygame.K_SPACE:
        flPause = not flPause
        if flPause:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    elif ev.key == pygame.K_LEFT:
        vol -= 0.1
        pygame.mixer.music.set_volume(vol)
    elif ev.key == pygame.K_RIGHT:
        vol += 0.1
        pygame.mixer.music.set_volume(vol)


def terminate():
    pygame.quit()
    sys.exit()


def play_music(name_music):
    pygame.mixer.music.load(name_music)
    pygame.mixer.music.play()


def start_screen_quiz():
    global width, height, event
    if end_game:
        play_music('data/end_game.mp3')
        intro_text = ["Игра окончена", "",
                      f"Вы набрали {points} баллов"]
    else:
        intro_text = ["Викторина", "",
                      "1 правильный ответ приносит 1 балл",
                      "Всего в викторине 2 уровня сложности",
                      'На каждом по 20 вопросов']
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
                    menu_quiz()
                return
        pygame.display.flip()


def level_quiz(difficulty_level):
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
    quiz()


def menu_quiz():
    global running, f, event, x, y, answers, suggest_hall
    answers = [1, 1, 1, 1]
    suggest_hall = False
    play_music("data/start_menu_music.mp3")
    f = open('data/question', encoding='utf-8', mode='r+')
    f = f.read().split('\n')
    screen.fill((0, 0, 15))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and (15 <= x <= 195 and 40 <= y <= 100):
                level_quiz(1)
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and (15 <= x <= 195 and 110 <= y <= 170):
                level_quiz(2)
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and (15 <= x <= 195 and 410 <= y <= 470):
                terminate()
            elif event.type == pygame.KEYDOWN:
                music_player(event)
        pygame.mixer.music.queue("data/menu_music.mp3")
        render_menu_quiz()
        pygame.display.flip()


def quiz():
    global event, running, x, y, timer, user_answer
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
                menu_quiz()
            elif event.type == pygame.KEYDOWN:
                music_player(event)
        timer -= clock.tick(1000) / 1000
        if int(timer) == 0:
            time_out()
        if user_answer != 0:
            checking_the_answer()
        pygame.mixer.music.queue("data/fon_music.mp3")
        render_quiz()
        pygame.display.flip()


def game_quiz():
    global width, height, screen
    width = 638
    height = 539
    screen = pygame.display.set_mode((width, height))
    start_screen_quiz()
    menu_quiz()


def render_start_menu(button):
    image = load_image('s1.jpg')
    screen.blit(image, (0, 0))
    image = load_image('s2.jpg')
    screen.blit(image, (125, 50))
    image = load_image('s2.jpg')
    screen.blit(image, (125, 160))
    if button == 1:
        image = load_image('s3.jpg')
        screen.blit(image, (125, 50))
    if button == 2:
        image = load_image('s3.jpg')
        screen.blit(image, (125, 160))
    image = load_image('s4.jpg')
    screen.blit(image, (171, 270))
    draw_text(200, 200, 30, "Викторина")
    draw_text(200, 200, 30, "Викторина")


def start_menu():
    global running, x, y, event
    button = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            x, y = pygame.mouse.get_pos()
            if 125 <= x <= 375 and 50 <= y <= 150:
                if not button:
                    play_music('data/button_sound_1.mp3')
                button = 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    play_music('data/button_sound_2.mp3')
                    pass
            elif 125 <= x <= 375 and 160 <= y <= 260:
                if not button:
                    play_music('data/button_sound_1.mp3')
                button = 2
                if event.type == pygame.MOUSEBUTTONDOWN:
                    play_music('data/button_sound_2.mp3')
                    game_quiz()
            else:
                button = 0

        render_start_menu(button)
        pygame.display.flip()


start_menu()
