"""Модуль логики и математической модели игры Тетрис."""

import random
from typing import List, Tuple, Optional


class TetrisModel:
    """Класс, описывающий игровое поле, фигуры и правила Тетриса."""

    SHAPES: List[Tuple[str, List[List[int]]]] = [
        ("#00F0F0", [[1, 1, 1, 1]]),               # I — голубой
        ("#F0F000", [[1, 1], [1, 1]]),             # O — желтый
        ("#A000F0", [[0, 1, 0], [1, 1, 1]]),       # T — фиолетовый
        ("#00F000", [[0, 1, 1], [1, 1, 0]]),       # S — зеленый
        ("#F00000", [[1, 1, 0], [0, 1, 1]]),       # Z — красный
        ("#0000F0", [[1, 0, 0], [1, 1, 1]]),       # J — синий
        ("#F0A000", [[0, 0, 1], [1, 1, 1]]),       # L — оранжевый
    ]

    def __init__(self, width: int = 10, height: int = 20) -> None:
        """Инициализирует игровое поле заданного размера.

        Args:
            width: Ширина в клетках.
            height: Высота в клетках.
        """
        self.width: int = width
        self.height: int = height
        self.grid: List[List[Optional[str]]] = []
        self.score: int = 0
        self.game_over: bool = False
        self.paused: bool = False

        self.current_shape: List[List[int]] = []
        self.current_color: str = "#FFFFFF"
        self.current_x: int = 0
        self.current_y: int = 0

        self.reset()

    def reset(self) -> None:
        """Сбрасывает игру в начальное состояние."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.game_over = False
        self.paused = False
        self._spawn_piece()

    def _spawn_piece(self) -> None:
        """Создает новую случайную фигуру в верхней части поля."""
        color, shape = random.choice(self.SHAPES)
        self.current_color = color
        self.current_shape = [row[:] for row in shape]
        self.current_x = self.width // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0

        if self._check_collision(self.current_shape, self.current_x, self.current_y):
            self.game_over = True

    def _check_collision(
        self, shape: List[List[int]], offset_x: int, offset_y: int
    ) -> bool:
        """Проверяет столкновение фигуры со стенами, дном или другими блоками.

        Args:
            shape: Матрица текущей фигуры.
            offset_x: Смещение по горизонтали.
            offset_y: Смещение по вертикали.

        Returns:
            True, если есть столкновение, иначе False.
        """
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = x + offset_x
                    new_y = y + offset_y
                    if (
                        new_x < 0
                        or new_x >= self.width
                        or new_y >= self.height
                        or (new_y >= 0 and self.grid[new_y][new_x] is not None)
                    ):
                        return True
        return False

    def move(self, dx: int, dy: int) -> bool:
        """Пытается сдвинуть текущую фигуру на заданное смещение.

        Args:
            dx: Смещение по оси X.
            dy: Смещение по оси Y.

        Returns:
            True, если движение успешно выполнено.
        """
        if self.game_over or self.paused:
            return False

        if not self._check_collision(
            self.current_shape, self.current_x + dx, self.current_y + dy
        ):
            self.current_x += dx
            self.current_y += dy
            return True
        return False

    def rotate(self) -> None:
        """Поворачивает текущую фигуру на 90 градусов по часовой стрелке."""
        if self.game_over or self.paused:
            return

        # Транспонирование матрицы и реверс строк для поворота на 90 градусов
        rotated = [
            list(row) for row in zip(*self.current_shape[::-1])
        ]
        if not self._check_collision(rotated, self.current_x, self.current_y):
            self.current_shape = rotated

    def step(self) -> None:
        """Выполняет один такт падения фигуры вниз."""
        if self.game_over or self.paused:
            return

        if not self.move(0, 1):
            self._lock_piece()
            self._clear_lines()
            self._spawn_piece()

    def _lock_piece(self) -> None:
        """Фиксирует упавшую фигуру в сетке игрового поля."""
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell and self.current_y + y >= 0:
                    self.grid[self.current_y + y][self.current_x + x] = self.current_color

    def _clear_lines(self) -> None:
        """Удаляет заполненные горизонтальные линии и начисляет очки."""
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        lines_cleared = self.height - len(new_grid)

        if lines_cleared > 0:
            # Начисление очков: 100, 300, 500 или 800 за 1-4 линии соответственно
            points = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += points.get(lines_cleared, lines_cleared * 200)
            empty_rows = [
                [None for _ in range(self.width)] for _ in range(lines_cleared)
            ]
            self.grid = empty_rows + new_grid

    def toggle_pause(self) -> None:
        """Переключает состояние паузы."""
        if not self.game_over:
            self.paused = not self.paused
