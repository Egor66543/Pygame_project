import os
import sys
import pygame


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

    draw_text(screen, 60, 90, 30, f[question_number])
    draw_text(screen, 130, 210, 30, f[question_number + 1])
    draw_text(screen, 130, 280, 30, f[question_number + 2])
    draw_text(screen, 130, 350, 30, f[question_number + 3])
    draw_text(screen, 130, 420, 30, f[question_number + 4])
    draw_text(screen, 70, 500, 30, f"points {str(points)}")


def checking_the_answer():
    global points, question_number, user_answer, running
    if user_answer == int(f[question_number + 5]):
        points += 1
    user_answer = 0
    if question_number == 240:
        running = False
    question_number += 6


pygame.init()

f = open('data/question', encoding='utf-8', mode='r')
f = f.read().split('\n')

points = 0
question_number = 0
user_answer = 0

width = 638
height = 539
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and (100 <= x <= 570 and 190 <= y <= 450):
            user_answer = (y - 190) // 65 + 1
        if event.type == pygame.MOUSEBUTTONDOWN and (0 <= x <= 60 and 480 <= y <= 540):
            question_number += 6
            if question_number == 240:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN and (578 <= x <= 638 and 480 <= y <= 540):
            running = False
    if user_answer != 0:
        checking_the_answer()
    render()
    pygame.display.flip()
