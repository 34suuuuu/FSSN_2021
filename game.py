import pygame  # 1. pygame 선언
from datetime import datetime
from datetime import timedelta

# pylint: disable=no-member

pygame.init()  # 2. pygame 초기화
pygame.display.set_caption('SNAKE GAME')

# 3. pygame에 사용되는 전역변수 선언
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
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

# 뱀 길이 = 20
def draw_block(screen, color, position):
    block = pygame.Rect((position[0] * 20, position[1] * 20),
                        (20, 20))
    pygame.draw.rect(screen, color, block)


class Snake:
    def __init__(self):
        self.positions = [(2, 0), (1, 0), (0, 0)]  # 뱀의 위치, (2,0이 머리)
        self.direction = ''

    def draw(self):
        for position in self.positions:
            draw_block(screen, GREEN, position)

    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'N':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'W':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(y, x + 1)] + self.positions[:-1]


class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)


# 4. pygame 무한루프


def runGame():
    global done, last_moved_time
    # 게임 시작 시, 뱀과 사과를 초기화
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

# 내가 한거
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

            print("collision ")
            print(snake.positions[0])

        snake.draw()
        apple.draw()
        pygame.display.update()


runGame()
pygame.quit()
