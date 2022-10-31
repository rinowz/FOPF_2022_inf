import pygame
from pygame.draw import circle, rect
pygame.init()

FPS = 30
# enter a gray background and set the colors
sc = pygame.display.set_mode((600, 600))

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
sc.fill(GRAY)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
RED = (255, 0, 0)

# general yellow circle
circle(sc, YELLOW,
                   (300, 250), 200)

circle(sc, BLACK,
                   (300, 250), 200, 1)
#left eye
circle(sc, RED,
                   (200, 180), 40)
circle(sc, BLACK,
                   (200, 180), 40, 1)


circle(sc, BLACK,
                   (200, 180), 15)
pygame.draw.polygon(sc, BLACK,
                    [[100, 70], [260, 120],
                     [250, 150], [90, 100]])




#right eye
circle(sc, RED,
                   (400, 180), 35)
circle(sc, BLACK,
                   (400, 180), 35, 1)

circle(sc, BLACK,
                   (400, 180), 15)

pygame.draw.polygon(sc, BLACK,
                    [[350, 130], [450, 110],
                     [460, 130], [360, 150]])

# LIPS
pygame.draw.polygon(sc, BLACK,
                    [[200, 350], [400, 350],
                     [400, 400], [200, 400]])





pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()