"""Модуль главного окна приложения и игрового цикла."""

import tkinter as tk
from src.models.tetris_model import TetrisModel
from src.renderers.renderer import TetrisRenderer


class TetrisApp:
    """Главный класс приложения, связывающий модель, рендерер и ввод пользователя."""

    TICK_MS: int = 450

    def __init__(self) -> None:
        """Инициализирует окно tkinter, модель и обработчики событий."""
        self.root = tk.Tk()
        self.root.title("Тетрис")
        self.root.resizable(False, False)

        self.model = TetrisModel(width=10, height=20)
        canvas_width = self.model.width * TetrisRenderer.CELL_SIZE
        canvas_height = self.model.height * TetrisRenderer.CELL_SIZE

        self.score_label = tk.Label(
            self.root, text="Счет: 0", font=("Arial", 14, "bold"), pady=8
        )
        self.score_label.pack()

        self.canvas = tk.Canvas(
            self.root,
            width=canvas_width,
            height=canvas_height,
            bg=TetrisRenderer.BG_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=(0, 10))

        self.renderer = TetrisRenderer(self.canvas, self.model)
        self._bind_events()

    def _bind_events(self) -> None:
        """Привязывает клавиши управления к действиям в игре."""
        self.root.bind("<Left>", lambda _: self._handle_move(-1, 0))
        self.root.bind("<Right>", lambda _: self._handle_move(1, 0))
        self.root.bind("<Down>", lambda _: self._handle_move(0, 1))
        self.root.bind("<Up>", lambda _: self._handle_rotate())
        self.root.bind("<space>", lambda _: self._handle_pause())
        self.root.bind("<r>", lambda _: self._handle_restart())
        self.root.bind("<R>", lambda _: self._handle_restart())

    def _handle_move(self, dx: int, dy: int) -> None:
        """Обрабатывает перемещение фигуры и обновляет экран."""
        if self.model.move(dx, dy):
            self.renderer.render()

    def _handle_rotate(self) -> None:
        """Обрабатывает поворот фигуры и обновляет экран."""
        self.model.rotate()
        self.renderer.render()

    def _handle_pause(self) -> None:
        """Ставит игру на паузу или снимает с неё."""
        self.model.toggle_pause()
        self.renderer.render()

    def _handle_restart(self) -> None:
        """Перезапускает игру."""
        self.model.reset()
        self._update_ui()

    def _update_ui(self) -> None:
        """Обновляет счет и перерисовывает игровое поле."""
        self.score_label.config(text=f"Счет: {self.model.score}")
        self.renderer.render()

    def _game_loop(self) -> None:
        """Выполняет периодический шаг игры."""
        self.model.step()
        self._update_ui()
        self.root.after(self.TICK_MS, self._game_loop)

    def run(self) -> None:
        """Запускает игровой цикл и главное окно."""
        self._update_ui()
        self.root.after(self.TICK_MS, self._game_loop)
        self.root.mainloop()
