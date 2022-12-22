import pygame
import sqlite3
import random


class Board:
    size = h, w = 850, 700
    screen = pygame.display.set_mode(size)
    con = sqlite3.connect("game_words.db")
    cur = con.cursor()
    id_word = cur.execute(f'''select id from words where id={random.randint(1, 10)}''').fetchone()[0]
    word = cur.execute(f'''SELECT word FROM words WHERE id={id_word}''').fetchone()[0]
    print(word)
    print(id_word)


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




