"""Точка входа для запуска игры Тетрис."""

from src.app import TetrisApp


def main() -> None:
    """Инициализирует и запускает главное окно приложения."""
    app = TetrisApp()
    app.run()


if __name__ == "__main__":
    main()
