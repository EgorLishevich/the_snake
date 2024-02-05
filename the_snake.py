from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTRE = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Все направления движения
DIRECTION = UP, DOWN, LEFT, RIGHT

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_SIZE), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс GameObject."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR) -> None:
        """Инициализация базовых атрибутов GameObject."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self, surface):
        """Метод определяющий как будет отрисован объект."""
        pass

    def paint(self, surface, position, body_color):
        """Отрисовка одной клетки на игрой поверхности."""
        rect = (
            pygame.Rect(
                (position), (GRID_SIZE, GRID_SIZE)
            )
        )
        pygame.draw.rect(surface, body_color, rect)

    def erase(self, surface, position):
        """Затирание одной клетки на игровой поверхности."""
        rect = (
            pygame.Rect(
                (position), (GRID_SIZE, GRID_SIZE)
            )
        )
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)


class Apple(GameObject):
    """Дочерний класс Apple."""

    def __init__(self, body_color=APPLE_COLOR) -> None:
        """Инициализация класса Apple."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Метод отвечающий за сучайное положение яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовка яблока."""
        self.paint(surface, self.position, self.body_color)


class Snake(GameObject):
    """Дочерний класс Snake."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR) -> None:
        """Инизиализация класса Snake."""
        super().__init__(body_color)
        self.body_color = SNAKE_COLOR
        self.handle_keys = choice(DIRECTION)
        self.reset()
        self.positions = [SCREEN_CENTRE]
        self.length = 1
        self.direction = RIGHT

    def draw(self, surface):
        """Метод отвечающий за отричовку головы и тела змеи,"""
        """а так же за удаление последнего элемента."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_position = self.get_head_position()
        self.paint(surface, head_position, self.body_color)

        if self.last:
            self.erase(surface, self.last)

    def update_direction(self):
        """Метод отвечающий за обновление направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод позволяющий получить позицию головы."""
        return self.positions[0]

    def reset(self):
        """Метод возвращающий змею в исходное положение."""
        self.length = 1
        self.positions = [SCREEN_CENTRE]
        self.next_direction = None
        self.direction = choice(DIRECTION)
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    def move(self):
        """Метод отвечающий за движение и рост змеи."""
        head_position = self.get_head_position()

        dx = (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        dy = (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        if len(self.positions) >= self.length:
            self.last = self.positions.pop()
            self.positions.insert(0, (dx, dy))
        elif len(self.positions) < self.length:
            self.positions.insert(0, (dx, dy))


def handle_keys(self):
    """Метод кправление объектами с помощью нажатия клавишь."""
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
    """Основной цикл игры."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        snake.update_direction()
        handle_keys(snake)
        snake.move()
        head_snake = snake.get_head_position()
        if head_snake in snake.positions[1:]:
            snake.reset()
        elif head_snake == apple.position:
            snake.length += 1
            apple.randomize_position()
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
