"""Модуль для работы с игровой доской."""
from typing import List, Tuple


class Board:
    """Класс для представления игровой доски."""

    # Константы для состояний клеток
    WATER = "~"
    SHIP = "S"
    HIT = "X"
    MISS = "O"

    def __init__(self, size: int = 6) -> None:
        """
        Инициализация доски.

        Args:
            size: Размер доски (по умолчанию 6x6)
        """
        self.size = size
        self.grid = self._create_empty_grid()
        self.ships_hit = 0

    def _create_empty_grid(self) -> List[List[str]]:
        """Создание пустой сетки доски.

        Returns:
            List[List[str]]: Пустая сетка заполненная '~'
        """
        return [[Board.WATER for _ in range(self.size)] 
                for _ in range(self.size)]

    def display(self, show_ships: bool = False) -> None:
        """Отображение доски в консоли.

        Args:
            show_ships: Показывать ли корабли (True) или скрывать их (False)
        """
        # Заголовок с номерами столбцов
        print("   " + " ".join(str(i) for i in range(self.size)))
        
        for i in range(self.size):
            row_display = []
            for cell in self.grid[i]:
                if cell == Board.SHIP and not show_ships:
                    row_display.append(Board.WATER)
                else:
                    row_display.append(cell)
            print(f"{i} |" + " ".join(row_display) + "|")

    def place_ship(
        self,
        row: int,
        col: int,
        size: int,
        horizontal: bool
    ) -> bool:
        """
        Размещение корабля на доске.

        Args:
            row: Начальная строка
            col: Начальный столбец
            size: Размер корабля
            horizontal: Горизонтальное размещение

        Returns:
            bool: Успешно ли размещен корабль
        """
        if not self._can_place_ship(row, col, size, horizontal):
            return False

        for i in range(size):
            current_row = row + (0 if horizontal else i)
            current_col = col + (i if horizontal else 0)
            self.grid[current_row][current_col] = Board.SHIP
        return True

    def _can_place_ship(
        self,
        row: int,
        col: int,
        size: int,
        horizontal: bool
    ) -> bool:
        """
        Проверка возможности размещения корабля.

        Args:
            row: Начальная строка
            col: Начальный столбец
            size: Размер корабля
            horizontal: Горизонтальное размещение

        Returns:
            bool: Можно ли разместить корабль
        """
        for i in range(size):
            current_row = row + (0 if horizontal else i)
            current_col = col + (i if horizontal else 0)

            # Проверка границ доски
            if current_row >= self.size or current_col >= self.size:
                return False

            # Проверка соседних клеток на наличие кораблей
            if not self._check_neighbors(current_row, current_col):
                return False

        return True

    def _check_neighbors(self, row: int, col: int) -> bool:
        """
        Проверка соседних клеток на наличие кораблей.

        Args:
            row: Строка для проверки
            col: Столбец для проверки

        Returns:
            bool: True если соседние клетки свободны
        """
        for delta_row in [-1, 0, 1]:
            for delta_col in [-1, 0, 1]:
                neighbor_row = row + delta_row
                neighbor_col = col + delta_col

                if (0 <= neighbor_row < self.size and 
                    0 <= neighbor_col < self.size):
                    if self.grid[neighbor_row][neighbor_col] == Board.SHIP:
                        return False
        return True

    def make_shot(self, row: int, col: int) -> str:
        """
        Выстрел по доске.

        Args:
            row: Строка для выстрела
            col: Столбец для выстрела

        Returns:
            str: Результат выстрела ('hit', 'miss' или 'invalid')
        """
        if not self._is_valid_coordinate(row, col):
            return "invalid"

        if self.grid[row][col] in [Board.HIT, Board.MISS]:
            return "invalid"

        if self.grid[row][col] == Board.SHIP:
            self.grid[row][col] = Board.HIT
            self.ships_hit += 1
            return "hit"

        self.grid[row][col] = Board.MISS
        return "miss"

    def _is_valid_coordinate(self, row: int, col: int) -> bool:
        """
        Проверка корректности координат.

        Args:
            row: Строка для проверки
            col: Столбец для проверки

        Returns:
            bool: True если координаты корректны
        """
        return 0 <= row < self.size and 0 <= col < self.size

    def count_ships(self) -> int:
        """Подсчет оставшихся кораблей на доске.

        Returns:
            int: Количество неподбитых кораблей
        """
        count = 0
        for row in self.grid:
            count += row.count(Board.SHIP)
        return count

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Получение списка пустых клеток.

        Returns:
            List[Tuple[int, int]]: Список координат пустых клеток
        """
        empty_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] not in [Board.HIT, Board.MISS]:
                    empty_cells.append((row, col))
        return empty_cells

    def clear_board(self) -> None:
        """Очистка доски (для новой игры)."""
        self.grid = self._create_empty_grid()
        self.ships_hit = 0