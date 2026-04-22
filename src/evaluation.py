from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class EvaluationCell:
    """
    Представляет оценку ячейки для алгоритмов принятия решений (например, ИИ).
    """
    row: int
    col: int
    value: float = 0.0  # Общая оценка приоритета хода
    value_x: float = 0.0  # Оценка значимости для игрока X
    value_o: float = 0.0  # Оценка значимости для игрока O
    max_x: float = 0.0    # длина собираемой комбинации X
    max_o: float = 0.0    # длина собираемой комбинации O
    is_empty_ends: bool = False  # true если собираемая комбинация имеет пустые концы

    def __str__(self):
        return f"({self.row}, {self.col}) | Value={self.value}, X={self.value_x}, O={self.value_o}, maxX={self.max_x}, maxO={self.max_o}"


class EvaluationLogic:
    """
    Класс, реализующий логику оценки игрового поля в игре "Крестики-нолики".
    Содержит методы для анализа линий (вертикальных, горизонтальных, диагональных)
    с целью определения последовательных совпадений символов игрока.
    """

    X = "X"
    O = "O"
    EMPTY = " "
    COUNT_WINNER = 5

    @staticmethod
    def get_value(cell_value: str, player: str) -> float:
        """
        Базовая функция оценки ячейки игрового поля.
        Возвращает 1, если значение ячейки совпадает с символом текущего игрока,
        0.5, если ячейка пуста, иначе возвращает 0.
        :param cell_value: Значение ячейки доски, которое необходимо оценить.
        :param player: Символ текущего игрока (например, "X" или "O"), с которым выполняется сравнение.
        :return: Оценка ячейки (1.0, 0.5 или 0.0).
        """
        if cell_value == player:
            return 1.0
        if cell_value == EvaluationLogic.EMPTY:
            return 0.5
        return 0.0

    def vertical_line(self, board, row: int, col: int, player: str) -> float:
        """
        Оценивает вертикальную линию на игровой доске, начиная с указанной позиции.
        Подсчитывает количество подряд идущих ячеек, содержащих символ текущего игрока,
        в направлениях вверх и вниз от заданной позиции. Подсчёт останавливается при встрече
        ячейки, не соответствующей символу игрока.
        :param board: Объект доски.
        :param row: Индекс строки центральной ячейки.
        :param col: Индекс столбца центральной ячейки.
        :param player: Символ текущего игрока (например, "X" или "O").
        :return: Суммарное количество подряд идущих ячеек, оценённых как 1 (совпадающих с player),
                 включая центральную ячейку. Минимальное возвращаемое значение — 1.
        """
        result = 1.0
        # Вверх
        temp_row = row - 1
        while temp_row >= 0:
            value = self.get_value(board.get_cell(temp_row, col), player)
            if value == 1.0:
                result += value
            else:
                if value > 0:
                    result += value
                break
            temp_row -= 1
        # Вниз
        temp_row = row + 1
        while temp_row < board.size:
            value = self.get_value(board.get_cell(temp_row, col), player)
            if value == 1.0:
                result += value
            else:
                if value > 0:
                    result += value
                break
            temp_row += 1
        return result

    def horizontal_line(self, board, row: int, col: int, player: str) -> float:
        """
        Оценивает горизонтальную линию на игровой доске, начиная с указанной позиции.
        Подсчитывает количество подряд идущих ячеек, содержащих символ текущего игрока,
        в направлениях влево и вправо от заданной позиции.
        :param board: Объект доски.
        :param row: Индекс строки центральной ячейки.
        :param col: Индекс столбца центральной ячейки.
        :param player: Символ текущего игрока (например, "X" или "O").
        :return: Суммарное количество подряд идущих ячеек, оценённых как 1.
        """
        result = 1.0
        # Влево
        temp_col = col - 1
        while temp_col >= 0:
            value = self.get_value(board.get_cell(row, temp_col), player)
            if value == 1.0:
                result += value
            else:
                if value > 0:
                    result += value
                break
            temp_col -= 1
        # Вправо
        temp_col = col + 1
        while temp_col < board.size:
            value = self.get_value(board.get_cell(row, temp_col), player)
            if value == 1.0:
                result += value
            else:
                if value > 0:
                    result += value
                break
            temp_col += 1
        return result

    def left_diagonal_line(self, board, row: int, col: int, player: str) -> float:
        """
        Оценивает левую диагональную линию (от верхнего левого к нижнему правому углу).
        :param board: Объект доски.
        :param row: Индекс строки центральной ячейки.
        :param col: Индекс столбца центральной ячейки.
        :param player: Символ текущего игрока (например, "X" или "O").
        :return: Суммарное количество подряд идущих ячеек, оценённых как 1.
        """
        result = 1.0
        # Вверх-влево
        temp_row, temp_col = row - 1, col - 1
        while temp_row >= 0 and temp_col >= 0:
            value = self.get_value(board.get_cell(temp_row, temp_col), player)
            if value == 1.0:
                result += value
            else:
                if value > 0:
                    result += value
                break
            temp_row -= 1
            temp_col -= 1
        # Вниз-вправо
        temp_row, temp_col = row + 1, col + 1
        while temp_row < board.size and temp_col < board.size:
            value = self.get_value(board.get_cell(temp_row, temp_col), player)
            if value == 1.0:
                result += value
            else:
                if value > 0:
                    result += value
                break
            temp_row += 1
            temp_col += 1
        return result

    def right_diagonal_line(self, board, row: int, col: int, player: str) -> float:
        """
        Оценивает правую диагональную линию (от нижнего левого к верхнему правому углу).
        :param board: Объект доски.
        :param row: Индекс строки центральной ячейки.
        :param col: Индекс столбца центральной ячейки.
        :param player: Символ текущего игрока (например, "X" или "O").
        :return: Суммарное количество подряд идущих ячеек, оценённых как 1.
        """
        result = 1.0
        # Вниз-влево
        temp_row, temp_col = row + 1, col - 1
        while temp_row < board.size and temp_col >= 0:
            value = self.get_value(board.get_cell(temp_row, temp_col), player)
            if value == 1.0:
                result += value
            else:
                if value > 0:
                    result += value
                break
            temp_row += 1
            temp_col -= 1
        # Вверх-вправо
        temp_row, temp_col = row - 1, col + 1
        while temp_row >= 0 and temp_col < board.size:
            value = self.get_value(board.get_cell(temp_row, temp_col), player)
            if value == 1.0:
                result += value
            else:
                if value > 0:
                    result += value
                break
            temp_row -= 1
            temp_col += 1
        return result

    def evaluation_next_move(self, board, row: int, col: int) -> EvaluationCell:
        """
        Оценивает приоритет следующего хода в указанной ячейке.
        :param board: Объект игрового поля.
        :param row: Строка ячейки.
        :param col: Столбец ячейки.
        :return: Оценка ячейки с учётом потенциала для X и O.
        """
        # Локальная функция для оценки по всем направлениям
        def evaluate_for_player(player):
            res_vert = self.vertical_line(board, row, col, player)
            res_hor = self.horizontal_line(board, row, col, player)
            res_left_d = self.left_diagonal_line(board, row, col, player)
            res_right_d = self.right_diagonal_line(board, row, col, player)

            total = res_vert + res_hor + res_left_d + res_right_d
            max_val = max(res_vert, res_hor, res_left_d, res_right_d)

            return total, max_val

        score_x, max_x = evaluate_for_player(self.X)
        score_o, max_o = evaluate_for_player(self.O)

        return EvaluationCell(row, col, score_x + score_o, score_x, score_o, max_x, max_o)

    def evaluation(self, board) -> List[EvaluationCell]:
        """
        Оценивает все пустые ячейки на доске и возвращает их оценки.
        :param board: Объект игрового поля.
        :return: Список оценённых ячеек.
        """
        empty_cells = board.get_empty_cells()
        evaluation_cells = []
        for row, col in empty_cells:
            evaluation = self.evaluation_next_move(board, row, col)
            evaluation_cells.append(evaluation)
        return evaluation_cells

    @staticmethod
    def sort_to_max_value(evaluation_cells: List[EvaluationCell]) -> List[EvaluationCell]:
        """
        Сортирует список оценочных ячеек по убыванию значения Value.
        :param evaluation_cells: Список оценённых ячеек.
        :return: Отсортированный список.
        """
        return sorted(evaluation_cells, key=lambda x: x.value, reverse=True)

    @staticmethod
    def sort_to_max_x(evaluation_cells: List[EvaluationCell]) -> List[EvaluationCell]:
        """
        Сортирует список оценочных ячеек по убыванию значения MaxX.
        :param evaluation_cells: Список оценённых ячеек.
        :return: Отсортированный список.
        """
        return sorted(evaluation_cells, key=lambda x: x.max_x, reverse=True)

    @staticmethod
    def sort_to_max_o(evaluation_cells: List[EvaluationCell]) -> List[EvaluationCell]:
        """
        Сортирует список оценочных ячеек по убыванию значения MaxO.
        :param evaluation_cells: Список оценённых ячеек.
        :return: Отсортированный список.
        """
        return sorted(evaluation_cells, key=lambda x: x.max_o, reverse=True)

    def next_move(self, board) -> EvaluationCell:
        """
        Определяет следующий ход для ИИ.
        :param board: Объект игрового поля.
        :return: Ячейка для следующего хода.
        """
        evaluation_cells = self.evaluation(board)
        if not evaluation_cells:
            raise ValueError("Нет доступных ходов")

        # Определяем текущую тактику
        max_x = max(cell.max_x for cell in evaluation_cells)
        max_o = max(cell.max_o for cell in evaluation_cells)

        # Если у соперника есть угроза, переходим в режим обороны
        if max_x > max_o:
            # Сортируем по max_x (блокировка)
            sorted_cells = self.sort_to_max_x(evaluation_cells)
        else:
            # Иначе атакуем
            sorted_cells = self.sort_to_max_o(evaluation_cells)

        return sorted_cells[0]