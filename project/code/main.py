"""Главный модуль для запуска игры Морской бой."""
from game import (
    Game,
    )


def main() -> None:
    """Главная функция запуска игры."""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\nИгра прервана. До свидания!")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")
        print("Пожалуйста, сообщите об этом разработчику.")


if __name__ == "__main__":
    main()