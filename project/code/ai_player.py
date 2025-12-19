"""Модуль для управления ИИ противника."""
import random
from typing import Tuple, Optional

from board import (
    Board,
    )
from ship_placer import (
    ShipPlacer,
    )
from player import (
    Player,
    )


class AIPlayer(Player):
    """Класс для управления ИИ противника."""

    def __init__(self) -> None:
        """
        Инициализация ИИ.
        """
        super().__init__("Компьютер")
        self.last_hit: Optional[Tuple[int, int]] = None
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.current_direction = 0
        self.hits_history: list[Tuple[int, int]] = []

    def make_shot(self, enemy_board: Board) -> Tuple[int, int]:
        """
        Выбор координат для выстрела ИИ.

        Args:
            enemy_board: Доска противника

        Returns:
            Tuple[int, int]: Координаты (строка, столбец) для выстрела
        """
        # Если был попадание, пытаемся добить корабль
        if self.last_hit:
            targeted_shot = self._make_targeted_shot(enemy_board)
            if targeted_shot:
                return targeted_shot

        # Иначе стреляем случайно
        return self._make_random_shot(enemy_board)

    def _make_random_shot(self, enemy_board: Board) -> Tuple[int, int]:
        """
        Случайный выстрел.

        Args:
            enemy_board: Доска противника

        Returns:
            Tuple[int, int]: Случайные координаты
        """
        empty_cells = enemy_board.get_empty_cells()

        if empty_cells:
            return random.choice(empty_cells)

        # Если все клетки обстреляны (крайний случай)
        return (0, 0)

    def _make_targeted_shot(self, enemy_board: Board) -> Optional[Tuple[int, int]]:
        """
        Целевой выстрел вокруг попадания.

        Args:
            enemy_board: Доска противника

        Returns:
            Optional[Tuple[int, int]]: Координаты для выстрела или None
        """
        if not self.last_hit:
            return None

        row, col = self.last_hit

        # Пробуем все направления вокруг попадания
        for _ in range(len(self.directions)):
            delta_row, delta_col = self.directions[self.current_direction]
            target_row = row + delta_row
            target_col = col + delta_col

            if (0 <= target_row < enemy_board.size and
                    0 <= target_col < enemy_board.size and
                    enemy_board.grid[target_row][target_col] not in 
                    [Board.HIT, Board.MISS]):
                return (target_row, target_col)

            # Меняем направление для следующей попытки
            self.current_direction = (self.current_direction + 1) % len(
                self.directions
            )

        # Если не нашли подходящую цель, сбрасываем
        self.last_hit = None
        self.current_direction = 0
        return None

    def register_result(self, row: int, col: int, result: str) -> None:
        """
        Регистрация результата выстрела.

        Args:
            row: Строка выстрела
            col: Столбец выстрела
            result: Результат выстрела
        """
        if result == "hit":
            self.hits_history.append((row, col))
            if not self.last_hit:
                self.last_hit = (row, col)
        elif result == "miss" and self.last_hit:
            # Меняем направление при промахе после попадания
            self.current_direction = (self.current_direction + 1) % len(
                self.directions
            )

    def place_ships(self, board: Board) -> None:
        """
        Разместить корабли на доске.

        Args:
            board: Доска для размещения
        """
        ships = [3, 2, 2, 1, 1, 1, 1]
        placer = ShipPlacer(board, ships)
        
        if not placer.auto_place():
            print("Ошибка: не удалось разместить корабли компьютера")
            # Попробуем очистить доску и разместить снова
            board.clear_board()
            placer.auto_place()

    def reset(self) -> None:
        """Сброс состояния ИИ."""
        self.last_hit = None
        self.current_direction = 0
        self.hits_history = []
        self.reset_score()