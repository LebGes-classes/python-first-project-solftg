"""Абстрактный класс для игроков."""
from abc import ABC, abstractmethod
from typing import Tuple

from board import (
    Board,
    )


class Player(ABC):
    """Абстрактный класс игрока."""

    def __init__(self, name: str) -> None:
        """
        Инициализация игрока.

        Args:
            name: Имя игрока
        """
        self.name = name
        self.score = 0

    @abstractmethod
    def make_shot(self, enemy_board: Board) -> Tuple[int, int]:
        """
        Сделать выстрел.

        Args:
            enemy_board: Доска противника

        Returns:
            Tuple[int, int]: Координаты выстрела
        """
        pass

    @abstractmethod
    def place_ships(self, board: Board) -> None:
        """
        Разместить корабли на доске.

        Args:
            board: Доска для размещения
        """
        pass

    def register_hit(self) -> None:
        """Зарегистрировать попадание."""
        self.score += 1

    def get_score(self) -> int:
        """
        Получить счет игрока.

        Returns:
            int: Количество попаданий
        """
        return self.score

    def reset_score(self) -> None:
        """Сбросить счет игрока."""
        self.score = 0