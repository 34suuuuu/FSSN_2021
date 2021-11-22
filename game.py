import pygame
from datetime import datetime
from datetime import timedelta
from pygame import mixer
import random
# pylint: disable=no-member

# Initialize pygame
pygame.init()
pygame.display.set_caption('SNAKE GAME')

# global
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
size = [600, 600]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()
last_moved_time = datetime.now()

KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}

# background music


def music_stop():
    pygame.mixer.music.stop()


def draw_block(screen, color, position):
    block = pygame.Rect((position[0] * 20, position[1] * 20),
                        (20, 20))
    pygame.draw.rect(screen, color, block)


class Snake:
    def __init__(self):
        self.positions = [(2, 0), (1, 0), (0, 0)]  # head - tail
        self.direction = ''

    def draw(self):
        for position in self.positions:
            draw_block(screen, GREEN, position)

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
        if self.direction == 'W':
            self.positions.append((x, y-1))
        if self.direction == 'E':
            self.positions.append((x, y+1))
        if self.direction == 'N':
            self.positions.append((x-1, y))
        if self.direction == 'S':
            self.positions.append((x+1, y))


class Apple:
    def __init__(self):
        position = (random.randrange(0, 25), random.randrange(0, 25))
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)


def runGame():
    global done, last_moved_time
    # Initialize Snake, Apple
    snake = Snake()
    apple = Apple()

    while not done:
        clock.tick(10)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

# keyboard
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         y, x = snake.positions[0]
        #         if event.type == pygame.K_LEFT:
        #             x += 1
        #         elif event.type == pygame.K_RIGHT:
        #             x -= 1
        #         elif event.type == pygame.K_UP:
        #             y -= 2
        #         elif event.type == pygame.K_DOWN:
        #             y += 2

        if timedelta(seconds=0.5) <= datetime.now() - last_moved_time:
            snake.move()

        if snake.positions[0] == apple.position:
            snake.eat()
            apple.position = (random.randrange(0, 25), random.randrange(0, 25))

        if snake.positions[0] == snake.positions[-1]:
            pygame.quit()

        snake.draw()
        apple.draw()
        pygame.display.update()


runGame()
pygame.quit()
