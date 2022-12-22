import pygame
import sqlite3
import random


class Board:
    size = h, w = 850, 700
    screen = pygame.display.set_mode(size)
    con = sqlite3.connect("game_words.db")
    cur = con.cursor()
    id_word = cur.execute(f'''select id from words where id={random.randint(1, 9)}''').fetchone()


if __name__ == '__main__':
    pygame.init()
    running = True
    screen = Board()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.display.flip()
    pygame.quit()




