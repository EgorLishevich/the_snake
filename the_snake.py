from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

DIRECTION = UP, DOWN, LEFT, RIGHT


# Тут опишите все классы игры.
class GameObject:

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        pass

    def paint(self, surface, position, body_color):
        rect = (
            pygame.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE)
            )
        )
        pygame.draw.rect(surface, body_color, rect)

    def erase(self, surface, position):
        rect = (
            pygame.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE)
            )
        )
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)


class Apple(GameObject):

    def __init__(self, body_color=APPLE_COLOR) -> None:
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        self.paint(surface, self.position, APPLE_COLOR)


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.handle_keys = choice(DIRECTION)
        self.reset()
        self.positions = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ]
        self.length = 1

    def draw(self, surface):
        for position in self.positions[:-1]:
            self.paint(surface, position, SNAKE_COLOR)

        head_position = self.positions[0]
        self.paint(surface, head_position, SNAKE_COLOR)

        # Затирание последнего сегмента
        if self.last:
            self.erase(surface, self.last)

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        ]
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    def move(self):
        head_position = self.get_head_position()

        if self.direction == UP:
            new_head_position = (
                head_position[0], head_position[1] - GRID_SIZE
            )

        elif self.direction == DOWN:
            new_head_position = (
                head_position[0], head_position[1] + GRID_SIZE
            )

        elif self.direction == LEFT:
            new_head_position = (
                head_position[0] - GRID_SIZE, head_position[1]
            )

        elif self.direction == RIGHT:
            new_head_position = (
                head_position[0] + GRID_SIZE, head_position[1]
            )

        if len(self.positions) >= self.length:
            self.last = self.positions.pop()
            self.positions.insert(0, new_head_position)
        elif len(self.positions) < self.length:
            self.positions.insert(0, new_head_position)


def handle_keys(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.next_direction = RIGHT


def main():

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        snake.update_direction()
        handle_keys(snake)
        snake.move()
        head_snake = snake.get_head_position()
        if (
            head_snake[0] < 0 or head_snake[0] >= SCREEN_WIDTH
            or head_snake[1] < 0 or head_snake[1] >= SCREEN_HEIGHT
        ):
            snake.reset()
        elif head_snake in snake.positions[1:]:
            snake.reset()
        elif head_snake == apple.position:
            snake.length += 1
            apple.randomize_position()
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
