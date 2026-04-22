from .board import Board
from .evaluation import EvaluationLogic

class Game:
    """
    Класс, управляющий игровым процессом в "Крестики-нолики".
    """

    def __init__(self, size=20):
        """
        Инициализирует новую игру.
        :param size: Размер игрового поля.
        """
        self.board = Board(size)
        self.evaluation_logic = EvaluationLogic()
        self.current_player = 'X'  # Игрок X всегда начинает
        
    def reset(self):
        """Сбрасывает игру к начальному состоянию."""
        self.board = Board(self.board.size)
        self.evaluation_logic = EvaluationLogic()
        self.current_player = 'X'

    def switch_player(self):
        """
        Переключает текущего игрока.
        """
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_player_move(self) -> bool:
        """
        Запрашивает у игрока ввод координат строки и столбца, проверяет их корректность
        и устанавливает символ на доску.
        :return: True, если ход успешно выполнен; иначе — False.
        """
        print(f"Ход игрока {self.current_player}")
        while True:
            try:
                row_input = input(f"Введите номер строки (0-{self.board.size-1}): ")
                if not row_input.strip():
                    print("Ввод не может быть пустым. Пожалуйста, введите число.")
                    continue
                row = int(row_input)
                if row < 0 or row >= self.board.size:
                    print(f"Номер строки должен быть в диапазоне от 0 до {self.board.size-1}.")
                    continue

                col_input = input(f"Введите номер столбца (0-{self.board.size-1}): ")
                if not col_input.strip():
                    print("Ввод не может быть пустым. Пожалуйста, введите число.")
                    continue
                col = int(col_input)
                if col < 0 or col >= self.board.size:
                    print(f"Номер столбца должен быть в диапазоне от 0 до {self.board.size-1}.")
                    continue

                if not self.board.make_move(row, col, self.current_player):
                    print("Ячейка уже занята. Выберите пустую ячейку.")
                    continue

                return True

            except ValueError:
                print("Некорректный ввод. Введите целое число.")
            except KeyboardInterrupt:
                print("\nИгра прервана пользователем.")
                return False

    def ai_move(self):
        """
        Выполняет ход искусственного интеллекта.
        """
        print("Ход искусственного интеллекта...")
        try:
            cell = self.evaluation_logic.next_move(self.board)
            self.board.make_move(cell.row, cell.col, self.current_player)
            print(f"ИИ сделал ход в ячейку ({cell.row}, {cell.col})")
        except ValueError as e:
            print(f"Ошибка ИИ: {e}")

    def play(self):
        """
        Запускает игровой цикл.
        """
        print("Добро пожаловать в игру Крестики-нолики на поле 20x20!")
        self.board.print_board()

        while True:
            if self.current_player == 'X':
                # Ход человека
                if not self.get_player_move():
                    print("Игра завершена.")
                    break
            else:
                # Ход ИИ
                self.ai_move()

            # Выводим обновлённое поле
            self.board.print_board()

            # Проверяем победителя
            if self.board.is_winner(self.current_player):
                print(f"Игрок {self.current_player} победил!")
                break

            # Проверяем ничью
            if self.board.is_full():
                print("Ничья!")
                break

            # Переключаем игрока
            self.switch_player()