"""Модуль отрисовки игрового поля и фигур на холсте tkinter."""

import tkinter as tk
from src.models.tetris_model import TetrisModel


class TetrisRenderer:
    """Класс, отвечающий за графическое отображение состояния игры."""

    CELL_SIZE: int = 30
    BG_COLOR: str = "#1E1E1E"
    GRID_COLOR: str = "#2D2D2D"

    def __init__(self, canvas: tk.Canvas, model: TetrisModel) -> None:
        """Инициализирует рендерер.

        Args:
            canvas: Холст tkinter для отрисовки.
            model: Экземпляр модели игры.
        """
        self.canvas = canvas
        self.model = model

    def render(self) -> None:
        """Полностью перерисовывает текущее состояние игры."""
        self.canvas.delete("all")
        self._draw_grid()
        self._draw_locked_blocks()
        if not self.model.game_over:
            self._draw_current_piece()
        self._draw_overlay()

    def _draw_grid(self) -> None:
        """Отрисовывает фоновую сетку игрового поля."""
        for y in range(self.model.height):
            for x in range(self.model.width):
                x1 = x * self.CELL_SIZE
                y1 = y * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=self.BG_COLOR, outline=self.GRID_COLOR
                )

    def _draw_cell(self, x: int, y: int, color: str) -> None:
        """Рисует один цветной блок фигурки.

        Args:
            x: Координата X в сетке.
            y: Координата Y в сетке.
            color: HEX-код цвета заливки.
        """
        x1 = x * self.CELL_SIZE + 1
        y1 = y * self.CELL_SIZE + 1
        x2 = (x + 1) * self.CELL_SIZE - 1
        y2 = (y + 1) * self.CELL_SIZE - 1
        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=color, outline="#FFFFFF", width=1
        )

    def _draw_locked_blocks(self) -> None:
        """Отрисовывает все зафиксированные на поле блоки."""
        for y, row in enumerate(self.model.grid):
            for x, color in enumerate(row):
                if color is not None:
                    self._draw_cell(x, y, color)

    def _draw_current_piece(self) -> None:
        """Отрисовывает падающую в данный момент фигуру."""
        for y, row in enumerate(self.model.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self._draw_cell(
                        self.model.current_x + x,
                        self.model.current_y + y,
                        self.model.current_color,
                    )

    def _draw_overlay(self) -> None:
        """Отрисовывает сообщения о паузе или окончании игры."""
        center_x = (self.model.width * self.CELL_SIZE) // 2
        center_y = (self.model.height * self.CELL_SIZE) // 2

        if self.model.game_over:
            self.canvas.create_rectangle(
                20, center_y - 40, self.model.width * self.CELL_SIZE - 20, center_y + 40,
                fill="#000000", outline="#FF4444", width=2
            )
            self.canvas.create_text(
                center_x, center_y - 10, text="ИГРА ОКОНЧЕНА",
                fill="#FF4444", font=("Arial", 16, "bold")
            )
            self.canvas.create_text(
                center_x, center_y + 15, text="Нажмите R для рестарта",
                fill="#FFFFFF", font=("Arial", 10)
            )
        elif self.model.paused:
            self.canvas.create_rectangle(
                40, center_y - 25, self.model.width * self.CELL_SIZE - 40, center_y + 25,
                fill="#000000", outline="#F0F000", width=2
            )
            self.canvas.create_text(
                center_x, center_y, text="ПАУЗА",
                fill="#F0F000", font=("Arial", 16, "bold")
            )
