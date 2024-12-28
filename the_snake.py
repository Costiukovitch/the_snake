from random import choice, randint

import pygame


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
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс GameObject - родительский, содержит общие атрибуты, инициализатор и метод для дочерних классов."""

    position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    body_color = (0, 0, 0)

    def __init__(self, object_position, object_color):
        """Инициализатор класса GameObject"""
        self.position = object_position
        self.color = object_color

    def draw():
        """Метод для отрисовки объектов на игровом поле, создан для переопределения в дочерних классах."""
        pass


class Snake(GameObject):
    """Класс Snake, содержит инициализатор, методы для обновления направления движения,
    перемещения по экрану, отрисовки, получения позиции "головы" 
    и метод для перезапуска игры."""

    def __init__(self, apple):
        """Инициализатор."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None
        self.apple_coords = apple.position

    def update_direction(self):
        """Метод для обновления направления движения после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """Метод для движение змейки с проверкой на съедение яблока."""
        self.last = self.positions[-1]
        current_position = self.get_head_position()

        for number in range(len(self.positions)):
            current_x, current_y = self.positions[number]
            move_x, move_y = self.direction
            if current_x // GRID_SIZE + move_x + 1 > GRID_WIDTH:
                new_coords = (0, current_y + move_y * GRID_SIZE)
            elif current_x // GRID_SIZE + move_x < 0:
                new_coords = (SCREEN_WIDTH - GRID_SIZE, current_y + move_y * GRID_SIZE)
            elif current_y // GRID_SIZE + move_y + 1 > GRID_HEIGHT:
                new_coords = (current_x + move_x * GRID_SIZE, 0)
            elif current_y // GRID_SIZE + move_y < 0:
                new_coords = (current_x + move_x * GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE)
            else:
                new_coords = (current_x + move_x * GRID_SIZE, current_y + move_y * GRID_SIZE)

            if new_coords in self.positions[2:]:
                self.reset(apple)

            if new_coords == self.apple_coords:
                while apple.position in self.positions:
                    apple.position = apple.randomize_position()
                self.apple_coords = apple.position
                self.length += 1

            self.positions.insert(number, new_coords)
            if len(self.positions) > self.length:
                self.positions.pop()
                break
            
    def draw(self):
        """Метод для отрисовки тела змейки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод для возвращения координат головы змейки."""
        return self.positions[0]
    
    def reset(self, apple):
        """Метод для перезапуска игры в случае столкновения."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.position = apple.randomize_position()
        self.apple_coords = apple.position


class Apple(GameObject):
    """Класс Apple, который содержит инициализатор, метод для отрисовки яблока
    и метод для создания координат яблока."""

    body_color = (255, 0, 0)
    position = (0, 0)

    def __init__(self):
        """Инициализатор."""
        self.color = (255, 0, 0)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Создание случайных координат для яблока."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return self.position

    def draw(self):
        """Метод для отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция для обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

def main():
    """Функция с основным игровым циклом"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake(apple)

    while True:
        clock.tick(SPEED)

        # Основная логика игры.
        handle_keys(snake)
        next_direction = snake.update_direction()
        snake.move(apple)
        snake.draw()

        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
