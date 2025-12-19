"""Основной модуль игры Морской бой."""
import os

from ai_player import (
    AIPlayer,
    )
from board import (
    Board,
    )
from human_player import (
    HumanPlayer,
    )



class Game:
    """Основной класс игры Морской бой."""

    def __init__(self) -> None:
        """Инициализация игры."""
        self.board_size = 6
        self.player: HumanPlayer
        self.computer: AIPlayer
        self.player_board: Board
        self.computer_board: Board
        self.player_view: Board

    def clear_screen(self) -> None:
        """Очистка экрана консоли."""
        os.system("cls" if os.name == "nt" else "clear")

    def display_menu(self) -> int:
        """Отображение главного меню.

        Returns:
            int: Выбранный пункт меню
        """
        self.clear_screen()
        print("=" * 60)
        print("МОРСКОЙ БОЙ".center(60))
        print("=" * 60)
        print("\nГлавное меню:")
        print("1. Начать новую игру")
        print("2. Правила игры")
        print("3. Выход")
        print("\n" + "=" * 60)

        while True:
            try:
                choice = int(input("\nВыберите пункт (1-3): "))
                if 1 <= choice <= 3:
                    return choice
                print("Пожалуйста, введите число от 1 до 3")
            except ValueError:
                print("Пожалуйста, введите корректное число")

    def display_rules(self) -> None:
        """Отображение правил игры."""
        self.clear_screen()
        print("=" * 60)
        print("ПРАВИЛА ИГРЫ".center(60))
        print("=" * 60)
        print("\nЦель игры:")
        print("• Первым потопить все корабли противника")
        print("\nПравила:")
        print("• Игра ведется на поле 6x6")
        print("• У каждого игрока 7 кораблей:")
        print("  - 1 корабль размером 3")
        print("  - 2 корабля размером 2")
        print("  - 4 корабля размером 1")
        print("• Корабли не могут соприкасаться")
        print("• Стреляйте, вводя координаты (строка, столбец)")
        print("\nОбозначения:")
        print(f"  {Board.WATER} - вода")
        print(f"  {Board.SHIP} - корабль (виден только на своей доске)")
        print(f"  {Board.HIT} - попадание")
        print(f"  {Board.MISS} - промах")
        print("\n" + "=" * 60)
        input("\nНажмите Enter для возврата в меню...")

    def setup_game(self) -> None:
        """Настройка игровых досок."""
        # Создаем игроков
        self.player = HumanPlayer()
        self.computer = AIPlayer()

        # Создаем доски
        self.player_board = Board(self.board_size)
        self.computer_board = Board(self.board_size)
        self.player_view = Board(self.board_size)

        # Расставляем корабли игрока
        print("\nИгрок расставляет корабли...")
        self.player.place_ships(self.player_board)

        # Расставляем корабли компьютера
        print("\nКомпьютер расставляет корабли...")
        self.computer.place_ships(self.computer_board)

    def display_game_state(self) -> None:
        """Отображение текущего состояния игры."""
        self.clear_screen()
        print("=" * 60)
        print("МОРСКОЙ БОЙ".center(60))
        print("=" * 60)

        print(f"\n{self.player.name}: {self.player.get_score()} попаданий")
        print(f"{self.computer.name}: {self.computer.get_score()} попаданий")

        print(f"\nДОСКА {self.player.name}:")
        self.player_board.display(show_ships=True)

        print(f"\nДОСКА {self.computer.name}:")
        self.player_view.display(show_ships=False)

        print("=" * 60)

    def player_turn(self) -> bool:
        """Ход игрока.

        Returns:
            bool: True если игрок попал и ходит снова
        """
        print(f"\nХод {self.player.name}")

        while True:
            row, col = self.player.make_shot(self.computer_board)

            result = self.computer_board.make_shot(row, col)

            if result == "invalid":
                print("Некорректный выстрел! Попробуйте еще раз.")
                continue

            # Обновляем вид игрока
            if result == "hit":
                self.player_view.grid[row][col] = Board.HIT
                self.player.register_hit()
                print("ПОПАДАНИЕ! ✅")
                return True

            self.player_view.grid[row][col] = Board.MISS
            print("ПРОМАХ! ❌")
            return False

    def computer_turn(self) -> bool:
        """Ход компьютера.

        Returns:
            bool: True если компьютер попал и ходит снова
        """
        print(f"\nХод {self.computer.name}")
        row, col = self.computer.make_shot(self.player_board)

        print(f"{self.computer.name} стреляет в [{row}, {col}]")

        result = self.player_board.make_shot(row, col)

        if result == "hit":
            print(f"{self.computer.name} попал в ваш корабль! 💥")
            self.computer.register_hit()
            self.computer.register_result(row, col, "hit")
            return True

        print(f"{self.computer.name} промахнулся")
        self.computer.register_result(row, col, "miss")
        return False

    def check_game_over(self) -> bool:
        """Проверка окончания игры.

        Returns:
            bool: True если игра окончена
        """
        player_ships_remaining = self.player_board.count_ships()
        computer_ships_remaining = self.computer_board.count_ships()

        return player_ships_remaining == 0 or computer_ships_remaining == 0

    def show_results(self) -> None:
        """Отображение результатов игры."""
        self.clear_screen()
        print("=" * 60)
        print("ИГРА ОКОНЧЕНА".center(60))
        print("=" * 60)

        player_ships_remaining = self.player_board.count_ships()
        computer_ships_remaining = self.computer_board.count_ships()

        print("\nФинальный счет:")
        print(f"{self.player.name}: {self.player.get_score()} попаданий")
        print(f"{self.computer.name}: {self.computer.get_score()} попаданий")
        print(f"\nКораблей {self.player.name} осталось: {player_ships_remaining}")
        print(f"Кораблей {self.computer.name} осталось: {computer_ships_remaining}")

        if computer_ships_remaining == 0:
            print("\n" + "=" * 60)
            print(f"ПОЗДРАВЛЯЮ! {self.player.name} ВЫИГРАЛ! 🎉".center(60))
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print(f"{self.computer.name} ВЫИГРАЛ! ПОПРОБУЙТЕ ЕЩЕ РАЗ! 💪".center(60))
            print("=" * 60)

        print(f"\nДоска {self.computer.name} (все корабли показаны):")
        self.computer_board.display(show_ships=True)

    def play_round(self) -> None:
        """Игровой раунд."""
        player_turn = True
        game_over = False

        while not game_over:
            self.display_game_state()

            if player_turn:
                hit = self.player_turn()
                if not hit:
                    player_turn = False
            else:
                hit = self.computer_turn()
                if not hit:
                    player_turn = True

            input("\nНажмите Enter для продолжения...")
            game_over = self.check_game_over()

    def ask_play_again(self) -> bool:
        """Спросить игрока, хочет ли он сыграть еще раз.

        Returns:
            bool: True если игрок хочет продолжить
        """
        while True:
            answer = input("\nХотите сыграть еще раз? (да/нет): ").lower()
            if answer in ["да", "д", "yes", "y"]:
                return True
            elif answer in ["нет", "н", "no", "n"]:
                return False
            print("Пожалуйста, ответьте 'да' или 'нет'")

    def reset_game(self) -> None:
        """Сброс состояния игры для новой партии."""
        # Очищаем доски
        if hasattr(self, 'player_board'):
            self.player_board.clear_board()
        if hasattr(self, 'computer_board'):
            self.computer_board.clear_board()
        if hasattr(self, 'player_view'):
            self.player_view.clear_board()

        # Сбрасываем счет игроков
        if hasattr(self, 'player'):
            self.player.reset_score()
        if hasattr(self, 'computer'):
            self.computer.reset()

    def run(self) -> None:
        """Основной цикл игры."""
        while True:
            choice = self.display_menu()

            if choice == 1:
                try:
                    self.setup_game()
                    self.play_round()
                    self.show_results()

                    if not self.ask_play_again():
                        print("\nСпасибо за игру! До свидания!")
                        return
                    else:
                        self.reset_game()

                except Exception as e:
                    print(f"\nПроизошла ошибка: {e}")
                    input("Нажмите Enter для продолжения...")
                    self.reset_game()

            elif choice == 2:
                self.display_rules()

            elif choice == 3:
                print("\nСпасибо за игру! До свидания!")
                return