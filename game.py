import os
import sys
import pygame
import random


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
clock = pygame.time.Clock()
running = False
timer = 0
timer_game = 0
f = []
hall_help_list = ['40%', '30%', '20%', '10%']
suggest_hall = False


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


def draw_text(screen, text_x, text_y, size, message_text):
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

    draw_text(screen, 60, 90, 30, f[question_number])
    if answers[0]:
        draw_text(screen, 130, 210, 30, f[question_number + 1])
    if answers[1]:
        draw_text(screen, 130, 280, 30, f[question_number + 2])
    if answers[2]:
        draw_text(screen, 130, 350, 30, f[question_number + 3])
    if answers[3]:
        draw_text(screen, 130, 420, 30, f[question_number + 4])
    if suggest_hall:
        if answers[0]:
            draw_text(screen, 540, 210, 30, hall_help_list[0])
        if answers[1]:
            draw_text(screen, 540, 280, 30, hall_help_list[1])
        if answers[2]:
            draw_text(screen, 540, 350, 30, hall_help_list[2])
        if answers[3]:
            draw_text(screen, 540, 420, 30, hall_help_list[3])

    draw_text(screen, 470, 500, 30, f"points {str(points)}")
    draw_text(screen, 360, 500, 30, f"Время {str(int(timer))}")


def render_menu():
    image = load_image('level_button.png')
    screen.blit(image, (15, 40))
    image = load_image('level_button.png')
    screen.blit(image, (15, 110))
    image = load_image('level_button.png')
    screen.blit(image, (15, 410))
    image = load_image('1.svg')
    screen.blit(image, (300, 20))
    draw_text(screen, 70, 60, 30, "Level 1")
    draw_text(screen, 70, 130, 30, "Level 2")
    draw_text(screen, 70, 430, 30, "Выход")


def checking_the_answer():
    global points, question_number, user_answer, running, end_game, answers
    if user_answer == int(f[question_number + 5]):
        points += 1
    user_answer = 0
    next_question()


def suggest_50_50():
    global suggest, question_number, answers
    pygame.mixer.music.load('data/50_50_music.mp3')
    pygame.mixer.music.play()
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
    pygame.mixer.music.load('data/hall_help.mp3')
    pygame.mixer.music.play()
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
    pygame.mixer.music.load('data/time-out.mp3')
    pygame.mixer.music.play()
    timer = timer_game
    next_question()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    if end_game:
        pygame.mixer.music.load('data/end_game.mp3')
        pygame.mixer.music.play()
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
        string_rendered = font.render(line, 1, pygame.Color('white'))
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
    pygame.mixer.music.load('data/level_selection_music.mp3')
    pygame.mixer.music.play()
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
    global running, f
    pygame.mixer.music.load("data/fon_music.mp3")
    pygame.mixer.music.play(-1)
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
        render_menu()
        pygame.display.flip()


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
    timer -= clock.tick(1000) / 1000
    if int(timer) == 0:
        time_out()
    if user_answer != 0:
        checking_the_answer()
    pygame.mixer.music.queue("data/fon_music.mp3")
    render()
    pygame.display.flip()
