import pygame
from pygame.draw import *
from random import randint
pygame.init()
b=900
a=1200
FPS = 30
screen = pygame.display.set_mode((a,b))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
Ex=[]
Ey=[]
Er=[]
col=[]
Espeedx=[]
Espeedy=[]
scope=0
t=5


def render(x, y, r, color):
    for i in range(len(x)):
        circle(screen, color[i], (x[i], y[i]), r[i])


def move(dt, Vx, Vy, x, y, r, a, b):
    for i in range(len(x)):
        if (a-x[i]) < r[i]:
            x[i] = a-r[i]
            Vx[i] = -Vx[i]
            x[i] += Vx[i] * t
        if (b-y[i]) < r[i]:
            Vy[i] = -Vy[i]
            y[i] += Vy[i] * t
            y[i] = b-r[i]
        if y[i] < r[i]:
            Vy[i] = -Vy[i]
            y[i] += Vy[i] * t
            y[i] = r[i]
        if x[i] < r[i]:
            Vx[i] = -Vx[i]
            x[i] += Vx[i] * t
            x[i] = r[i]


        else:
            x[i] += Vx[i]*t
            y[i] += Vy[i]*t



def remember():
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    Ex.append(x)
    Ey.append(y)
    Er.append(r)
    col.append(color)
    Vx = randint(-5,5)
    Vy = randint(-5,5)
    Espeedx.append(Vx)
    Espeedy.append(Vy)




pygame.display.update()
clock = pygame.time.Clock()
finished = False

wait_time = 1
frame_counter = 0
while not finished:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    if frame_counter % (FPS * wait_time) == 0:
        remember()
        render(ballx, bally, ballr, remcol)
    render(ballx, bally, ballr, remcol)
    move(dt, ballspeedx, ballspeedy, ballx, bally, ballr, a, b)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(ballx)):
                if (ballx[i] - event.pos[0]) ** 2 + (bally[i] - event.pos[1]) ** 2 <= ballr[i]**2:
                    ballx.pop(i)
                    bally.pop(i)
                    ballr.pop(i)
                    remcol.pop(i)
                    ballspeedy.pop(i)
                    ballspeedx.pop(i)

                    scope += 1
                    print('Click!')

                    break

    frame_counter += 1
print(scope)
pygame.quit()