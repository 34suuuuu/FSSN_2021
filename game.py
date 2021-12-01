import pygame
from datetime import datetime
from datetime import timedelta
import random
from network import Network
import time
from time import sleep
# pylint: disable=no-member

# Initialize pygame
pygame.init()
pygame.display.set_caption('SNAKE GAME🐍')

# global
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 8, 80)

font = pygame.font.SysFont("FixedSsy", 30, True, False)
font_large = pygame.font.SysFont("FixedSsy", 70, True, False)

size = [520, 520]
screen = pygame.display.set_mode(size)
score_player = 0

done = False
clock = pygame.time.Clock()
last_moved_time = datetime.now()

KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}


def draw_gameover(screen):
    text_gameover = font_large.render("GAME OVER", True,  YELLOW)
    screen.blit(text_gameover, (size[0]//2 - text_gameover.get_width()//2,
                                size[1]//2 - text_gameover.get_height()//2))


def draw_block(screen, color, position):
    block = pygame.Rect((position[0] * 20, position[1] * 20),
                        (20, 20))
    pygame.draw.rect(screen, color, block)


# 화면에 점수 나타내기
def draw_score(screen, score_player):
    text_score = font.render("Score: " + str(score_player), True, WHITE)
    screen.blit(text_score, (15, 15))


# 화면에 잔여 시간 나타내기
def draw_time(screen, start_time, score_player):
    remain_time = 20 - (int(time.time()) - start_time)

    if remain_time <= 0:
        remain_time = 0
        text_score = font_large.render(
            "Score: "+str(score_player), True,  YELLOW)
        screen.blit(text_score, (size[0]//2 - text_score.get_width()//2,
                    size[1]//2 - text_score.get_height()//2))
    text_time = font.render("Time: " + str(remain_time), True, WHITE)
    screen.blit(text_time, (390, 15))

# single인지 multi인지 선택하기위한 버튼 표시


def draw_button(screen, text, x, y):
    text_player = font_large.render(str(text), True, WHITE)
    screen.blit(text_player, (x, y))


class Button:
    def __init__(self, text, y):
        self.text = text
        self.y = y
        self.font = pygame.font.SysFont("FixedSsy", 70, True, False)
        self.text_button = self.font.render(self.text, True, WHITE)

    def draw(self):
        screen.blit(self.text_button, (size[0] // 2 - self.text_button.get_width() //
                    2, self.y))

    def click(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        sw = size[0]//2 - self.text_button.get_width()//2
        lw = size[0]//2 + self.text_button.get_width()//2

        lh = self.y + self.text_button.get_height()
        sh = self.y

        if click[0]:
            if (mouse[0] < lw) and (mouse[0] > sw):
                if mouse[1] < lh and mouse[1] > sh:
                    return click[0]


class Snake:
    def __init__(self, color):
        self.positions = [(2, 24), (1, 24), (0, 24)]  # head - tail
        # self.x = x
        # self.y = y
        self.direction = ''
        self.color = color

    def draw(self):
        for position in self.positions:
            draw_block(screen, self.color, position)

    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'W':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'N':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(y, x + 1)] + self.positions[:-1]

    def eat(self):
        tail_position = self.positions[-1]
        x, y = tail_position

        if len(self.positions) <= 8:
            if self.direction == 'W':
                self.positions.append((x, y-1))
            elif self.direction == 'E':
                self.positions.append((x, y+1))
            elif self.direction == 'N':
                self.positions.append((x-1, y))
            elif self.direction == 'S':
                self.positions.append((x+1, y))


class Apple:
    def __init__(self):
        position = (random.randrange(1, 25), random.randrange(1, 25))
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)


def runGame():
    global done, last_moved_time, score_player, client

    # Initialize Snake, Apple, Button
    snake = Snake(GREEN)
    apple = Apple()
    apple2 = Apple()
    n = Network()

    start_time = int(time.time())

    while not done:
        clock.tick(10)

        # 뱀이 사과를 먹으면 점수 추가, 사과 위치 랜덤
        if snake.positions[0] == apple.position:
            score_player += 1
            snake.eat()
            apple.position = (random.randrange(1, 25), random.randrange(2, 12))
            n.send(str(score_player))

        elif snake.positions[0] == apple2.position:
            score_player += 1
            snake.eat()
            apple2.position = (random.randrange(
                1, 25), random.randrange(12, 25))
            n.send(str(score_player))

        # 머리가 몸통이랑 만나면 게임 종료
        if snake.positions[0] in snake.positions[1:]:
            done = True

        # 벽과 부딪히면 게임 종료
        if (snake.positions[0][0] > 25) or (snake.positions[0][0] < 0) or (snake.positions[0][1] > 25) or (snake.positions[0][1] < 0):
            draw_gameover(screen)
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        if timedelta(seconds=0.5) <= datetime.now() - last_moved_time:
            snake.move()

        screen.fill(BACKGROUND)
        snake.draw()
        apple.draw()
        apple2.draw()
        draw_score(screen, score_player)
        draw_time(screen, start_time, score_player)

        pygame.display.update()


def runButton():
    screen.fill(BACKGROUND)
    n = Network()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        button1.draw()
        button2.draw()

        if button1.click() == True:
            n.send(str(button1.text))
            break
        if button2.click() == True:
            n.send(str(button2.text))
            break

        clock.tick(30)
        pygame.display.update()


button1 = Button("Single Player", 150)
button2 = Button("Multi Player", 300)

runButton()
runGame()
pygame.quit()
