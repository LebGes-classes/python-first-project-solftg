"""Модуль для размещения кораблей на доске."""
import random
from typing import List

from board import (
    Board,
    )


class ShipPlacer:
    """Класс для размещения кораблей на доске."""

    def __init__(self, board: Board, ships: List[int]) -> None:
        """
        Инициализация разместителя кораблей.

        Args:
            board: Доска для размещения
            ships: Список размеров кораблей
        """
        self.board = board
        self.ships = ships

    def auto_place(self) -> bool:
        """Автоматическое размещение всех кораблей.

        Returns:
            bool: Успешно ли размещены все корабли
        """
        for ship_size in self.ships:
            if not self._place_single_ship(ship_size):
                return False
        return True

    def _place_single_ship(self, ship_size: int) -> bool:
        """Размещение одного корабля.

        Args:
            ship_size: Размер корабля

        Returns:
            bool: Успешно ли размещен корабль
        """
        max_attempts = 100
        attempts = 0

        while attempts < max_attempts:
            horizontal = random.choice([True, False])
            row = random.randint(0, self.board.size - 1)
            col = random.randint(0, self.board.size - 1)

            if self.board.place_ship(row, col, ship_size, horizontal):
                return True

            attempts += 1

        return False

    def manual_place_ship(
        self,
        ship_size: int,
        row: int,
        col: int,
        horizontal: bool
    ) -> bool:
        """
        Ручное размещение одного корабля.

        Args:
            ship_size: Размер корабля
            row: Строка для размещения
            col: Столбец для размещения
            horizontal: Горизонтальное размещение

        Returns:
            bool: Успешно ли размещен корабль
        """
        return self.board.place_ship(row, col, ship_size, horizontal)