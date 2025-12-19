"""Модуль для управления человеческим игроком."""
from typing import Tuple

from board import (
    Board,
    )
from ship_placer import (
    ShipPlacer,
    )
from player import (
    Player,
    )


class HumanPlayer(Player):
    """Класс для управления человеческим игроком."""

    def __init__(self, name: str = "Игрок") -> None:
        """
        Инициализация человеческого игрока.

        Args:
            name: Имя игрока
        """
        super().__init__(name)

    def make_shot(self, enemy_board: Board) -> Tuple[int, int]:
        """
        Сделать выстрел (ввод от пользователя).

        Args:
            enemy_board: Доска противника

        Returns:
            Tuple[int, int]: Координаты выстрела
        """
        while True:
            try:
                row = int(input("Введите номер строки (0-5): "))
                col = int(input("Введите номер столбца (0-5): "))

                if not (0 <= row < enemy_board.size and 
                        0 <= col < enemy_board.size):
                    print("Координаты вне диапазона! Попробуйте снова.")
                    continue

                return (row, col)

            except ValueError:
                print("Пожалуйста, введите корректные числа!")

    def place_ships(self, board: Board) -> None:
        """
        Разместить корабли на доске.

        Args:
            board: Доска для размещения
        """
        ships = [3, 2, 2, 1, 1, 1, 1]

        print("\nВыберите режим расстановки:")
        print("1. Автоматическая расстановка")
        print("2. Ручная расстановка")

        while True:
            try:
                choice = int(input("Ваш выбор (1-2): "))
                if choice == 1:
                    self._auto_place_ships(board, ships)
                    return
                elif choice == 2:
                    self._manual_place_ships(board, ships)
                    return
                print("Пожалуйста, введите 1 или 2")
            except ValueError:
                print("Пожалуйста, введите корректное число")

    def _auto_place_ships(self, board: Board, ships: list[int]) -> None:
        """
        Автоматическая расстановка кораблей.

        Args:
            board: Доска для размещения
            ships: Список размеров кораблей
        """
        placer = ShipPlacer(board, ships)
        if placer.auto_place():
            print("\nКорабли успешно расставлены!")
        else:
            print("\nОшибка при расстановке кораблей!")
        input("\nНажмите Enter для продолжения...")

    def _manual_place_ships(self, board: Board, ships: list[int]) -> None:
        """
        Ручная расстановка кораблей.

        Args:
            board: Доска для размещения
            ships: Список размеров кораблей
        """
        print("\nРучная расстановка кораблей")
        print("Корабли для размещения:", ships)

        placer = ShipPlacer(board, ships)

        for ship_size in ships:
            self._display_placement_board(board)
            self._place_single_ship_manual(placer, ship_size)

    def _display_placement_board(self, board: Board) -> None:
        """
        Отображение доски во время расстановки.

        Args:
            board: Доска для отображения
        """
        print("\nВАША ДОСКА:")
        board.display(show_ships=True)

    def _place_single_ship_manual(self, placer: ShipPlacer, 
                                  ship_size: int) -> None:
        """
        Ручное размещение одного корабля.

        Args:
            placer: Объект для размещения кораблей
            ship_size: Размер корабля для размещения
        """
        placed = False
        while not placed:
            print(f"\nРазмещаем корабль размером {ship_size}")

            try:
                row = int(input("Введите номер строки (0-5): "))
                col = int(input("Введите номер столбца (0-5): "))
                direction = input("Горизонтально (г) или Вертикально (в)? ")

                horizontal = direction.lower() in ["г", "g", "h", "гор", "horizontal"]

                if placer.manual_place_ship(row, col, ship_size, horizontal):
                    placed = True
                    print(f"Корабль размером {ship_size} размещен!")
                else:
                    print("Нельзя разместить корабль здесь! Попробуйте еще раз.")

            except (ValueError, IndexError):
                print("Некорректный ввод! Попробуйте еще раз.")