# НЕОБХОДИМО ТАКЖЕ ЗАГРУЗИТЬ ФАЙЛ est.mp3
import math
from random import choice
from random import randint as rnd
import time


import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
k = 0.8


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        
        self.x += self.vx
        self.y -= self.vy
        
        if (self.x <= self.r):
            self.vx *= -k
            self.vy *= k
            self.x = self.r
        elif (self.x + self.r >= WIDTH):
            self.vx *= -k
            self.vy *= k
            self.x = WIDTH - self.r
            
        if (self.y <= self.r):
            self.vy *= -k
            self.vx *= k
            self.y = self.r
        elif (self.y + self.r >= HEIGHT):
            self.vy *= -k
            self.vx *= k
            self.y = HEIGHT - self.r

        self.vy -= 10/FPS
        
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (((self.r + obj.r)**2) >=
            ((self.x - obj.x)**2 + (self.y - obj.y)**2)):
            return True
        
        return False
    

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.rect(
            self.screen,
            self.color,
            (30, 445, 20, 10)
        )
        x = (math.sin(self.an)*5)
        y = (math.cos(self.an)*5)
        lx = (math.cos(self.an)*self.f2_power)
        ly = (math.sin(self.an)*self.f2_power)
        pygame.draw.polygon(self.screen, self.color,
                            [[40+x,450-y],
                             [40+lx+x,450+ly-y],[40+lx-x,450+ly+y],[40-x,450+y]])
            
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target():
    # self.points = 0
    # self.live = 1

    def __init__(self, screen):
        """ Call functions when object is created. """
        self.screen = screen
        self.r = rnd(2, 50)
        self.color = RED
        self.points = 0
        self.live = 1
        self.d = rnd(35,60)
        self.w = rnd(1,10)
        self.phi = 0
        self.x0 = rnd(600, 780)
        self.y0 = rnd(300, 550)
        self.x = self.x0
        self.y = self.y0
    
    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
    
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
    
    def move(self):
        self.x = self.x0 + self.d * math.cos(self.phi)
        self.y = self.y0 + self.d * math.sin(self.phi)
        self.phi += self.w/FPS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f = pygame.font.Font(None, 30)


bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
targets = [target1,target2]
finished = False
exist = False
times = f.render('', True, BLACK)


while not finished:
    
    screen.fill(WHITE)
    gun.draw()
    for targ in targets:
        targ.draw()
    for b in balls:
        b.draw()
    tscore = f.render(f'{target1.points+target2.points}', True, BLACK)
    screen.blit(tscore, (30,30))
    if exist:
        screen.blit(times, (300,30))
        pygame.display.update()
        time.sleep(1)
        exist = False
    pygame.display.update()
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        for targ in targets:
            targ.move()
            if b.hittest(targ) and targ.live:
                exist = True
                if len(balls) != 0:
                    times = f.render(f'Вы уничтожили цель за {len(balls)} выстрел(а)', True, BLACK)
                targ.live = 0
                targ.hit()
                targ.new_target()
                balls.clear()

                pygame.mixer.music.load("est.mp3")
                pygame.mixer.music.play(1)
        
    gun.power_up()

pygame.quit()