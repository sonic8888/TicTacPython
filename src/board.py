class Board:
    """
    Класс, представляющий игровое поле для игры "Крестики-нолики".
    """

    def __init__(self, size=20):
        """
        Инициализирует игровое поле заданного размера.
        :param size: Размер стороны квадратного поля (по умолчанию 20).
        """
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]

    def is_empty(self, row, col):
        """
        Проверяет, пуста ли ячейка на заданных координатах.
        :param row: Номер строки.
        :param col: Номер столбца.
        :return: True, если ячейка пуста, иначе False.
        """
        return self.grid[row][col] == ' '

    def make_move(self, row, col, player):
        """
        Устанавливает символ игрока в указанную ячейку, если она пуста.
        :param row: Номер строки.
        :param col: Номер столбца.
        :param player: Символ игрока ('X' или 'O').
        :return: True, если ход выполнен успешно, иначе False.
        """
        if 0 <= row < self.size and 0 <= col < self.size and self.is_empty(row, col):
            self.grid[row][col] = player
            return True
        return False

    def is_full(self):
        """
        Проверяет, заполнено ли игровое поле.
        :return: True, если все ячейки заняты, иначе False.
        """
        return all(self.grid[i][j] != ' ' for i in range(self.size) for j in range(self.size))

    def print_board(self):
        """
        Выводит игровое поле в консоль с отображением индексов строк и столбцов.
        """
        # Печать заголовков столбцов
        print("  " + "".join(f" {i} " for i in range(self.size)))
        for i in range(self.size):
            # Печать индекса строки и содержимого ячеек
            row_str = "|".join(self.grid[i][j] for j in range(self.size))
            print(f"{i} {row_str}_")

    def get_empty_cells(self):
        """
        Возвращает список координат всех пустых ячеек на поле.
        :return: Список кортежей (row, col) пустых ячеек.
        """
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.is_empty(i, j)]

    def get_cell(self, row, col):
        """
        Возвращает значение в указанной ячейке.
        :param row: Номер строки.
        :param col: Номер столбца.
        :return: Символ в ячейке ('X', 'O' или ' ').
        """
        return self.grid[row][col]

    def is_winner(self, player):
        """
        Проверяет, есть ли победитель для заданного игрока.
        :param player: Символ игрока ('X' или 'O').
        :return: Кортеж (bool, list), где bool - наличие победителя, list - координаты победной линии.
        """
        for row in range(self.size):
            for col in range(self.size):
                result, line = self._check_line(row, col, player)
                if result:
                    return True, line
        return False, []

    def _check_line(self, row, col, player):
        """
        Проверяет, есть ли победная комбинация, начинающаяся с заданной ячейки.
        :param row: Номер строки начала проверки.
        :param col: Номер столбца начала проверки.
        :param player: Символ игрока ('X' или 'O').
        :return: Кортеж (bool, list), где bool - наличие победной комбинации, list - координаты пяти ячеек.
        """
        directions = [
            (0, 1),   # Горизонтально
            (1, 0),   # Вертикально
            (1, 1),   # Диагонально вправо вниз
            (1, -1)   # Диагонально влево вниз
        ]
        for d_row, d_col in directions:
            line = []
            for i in range(5):
                r, c = row + i * d_row, col + i * d_col
                if 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == player:
                    line.append((r, c))
                else:
                    break
            if len(line) == 5:
                return True, line
        return False, []