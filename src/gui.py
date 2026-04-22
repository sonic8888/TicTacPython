import tkinter as tk
from tkinter import messagebox
from .game import Game
from .board import Board
import time

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики 20x20")
        self.root.resizable(False, False)
        
        # Игровая логика
        self.game = Game(size=20)
        self.board = self.game.board
        
        # Параметры сетки
        self.cell_size = 30
        self.grid_width = self.board.size * self.cell_size
        self.grid_height = self.board.size * self.cell_size
        
        # Холст для рисования
        self.canvas = tk.Canvas(
            self.root, 
            width=self.grid_width, 
            height=self.grid_height,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Кнопка Новая игра
        self.new_game_button = tk.Button(
            self.root, 
            text="Новая игра", 
            font=("Arial", 12),
            command=self.start_new_game
        )
        self.new_game_button.pack(pady=10)
        
        # Словарь для хранения анимаций символов
        self.animations = {}  # (row, col): {'symbol': 'X'/'O', 'progress': float}
        
        # Переменные для анимации победной линии
        self.win_line_start = None
        self.win_line_end = None
        self.win_line_progress = 0.0
        self.winning_line = []
        
        # Состояние игры
        self.game_active = True
        
        # Привязка события клика
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Рисуем начальную сетку
        self.draw_grid()
        
    def draw_grid(self):
        """Рисует сетку 20x20"""
        self.canvas.delete("grid")  # Очищаем старую сетку
        
        # Вертикальные линии
        for col in range(self.board.size + 1):
            x = col * self.cell_size
            self.canvas.create_line(
                x, 0, x, self.grid_height,
                fill="white", width=1, tags="grid"
            )
        
        # Горизонтальные линии
        for row in range(self.board.size + 1):
            y = row * self.cell_size
            self.canvas.create_line(
                0, y, self.grid_width, y,
                fill="white", width=1, tags="grid"
            )
        
    def get_cell_center(self, row, col):
        """Возвращает центр ячейки"""
        x = (col + 0.5) * self.cell_size
        y = (row + 0.5) * self.cell_size
        return x, y
        
    def on_canvas_click(self, event):
        """Обработчик клика по холсту"""
        if not self.game_active:
            return
            
        # Определяем ячейку по координатам
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Проверяем границы и доступность ячейки
        if (0 <= row < self.board.size and 
            0 <= col < self.board.size and 
            self.board.is_empty(row, col)):
            
            # Ход игрока X
            if self.game.current_player == 'X':
                self.board.make_move(row, col, 'X')
                self.animations[(row, col)] = {'symbol': 'X', 'progress': 0}
                self.animate_symbol(row, col)
                
                # Проверка победы
                is_winner, winning_line = self.board.is_winner('X')
                if is_winner:
                    self.game_active = False
                    self.winning_line = winning_line
                    self.animate_winning_line()
                    return
                
                # Переключаем игрока и ход ИИ
                self.game.switch_player()
                self.root.after(500, self.ai_move)

    def ai_move(self):
        """Выполняет ход ИИ"""
        if not self.game_active or self.game.current_player != 'O':
            return
            
        # Получаем ход от ИИ
        try:
            cell = self.game.evaluation_logic.next_move(self.board)
            row, col = cell.row, cell.col
            
            if self.board.make_move(row, col, 'O'):
                self.animations[(row, col)] = {'symbol': 'O', 'progress': 0}
                self.animate_symbol(row, col)
                
                # Проверка победы
                is_winner, winning_line = self.board.is_winner('O')
                if is_winner:
                    self.game_active = False
                    self.winning_line = winning_line
                    self.animate_winning_line()
                    return
                
                # Переключаем игрока
                self.game.switch_player()
                
        except ValueError:
            # Нет доступных ходов
            self.game_active = False
            self.root.after(100, lambda: messagebox.showinfo("Ничья!", "Ничья!"))

    def animate_symbol(self, row, col):
        """Анимирует отрисовку символа"""
        if (row, col) not in self.animations:
            return
            
        symbol = self.animations[(row, col)]['symbol']
        progress = self.animations[(row, col)]['progress']
        
        # Очищаем предыдущую отрисовку символа
        self.canvas.delete(f"symbol_{row}_{col}")
        
        if symbol == 'X':
            self.animate_cross(row, col, progress)
        elif symbol == 'O':
            self.animate_circle(row, col, progress)
        
        # Обновляем прогресс
        progress += 0.05  # Скорость анимации
        self.animations[(row, col)]['progress'] = min(progress, 1.0)
        
        # Продолжаем анимацию
        if progress < 1.0:
            self.root.after(50, lambda: self.animate_symbol(row, col))
        else:
            # Если анимация символа завершена, проверяем победу
            is_winner, winning_line = self.board.is_winner(self.game.current_player)
            if is_winner and self.game_active:
                self.game_active = False
                self.winning_line = winning_line
                self.animate_winning_line()
        
    def animate_cross(self, row, col, progress):
        """Анимированная отрисовка крестика"""
        x, y = self.get_cell_center(row, col)
        
        # Размер крестика (80% от размера ячейки)
        size = self.cell_size * 0.8
        half_size = size / 2
        
        # Координаты для диагоналей
        x1, y1 = x - half_size, y - half_size  # Верхний левый
        x2, y2 = x + half_size, y + half_size  # Нижний правый
        
        # Первая диагональ: сверху слева - вниз справа
        progress1 = min(1.0, progress * 2.0)
        end_x1 = x1 + (x2 - x1) * progress1
        end_y1 = y1 + (y2 - y1) * progress1
        
        self.canvas.create_line(
            x1, y1, end_x1, end_y1,
            fill="yellowgreen", width=4, capstyle="round",
            tags=f"symbol_{row}_{col}"
        )
        
        # Вторая диагональ: сверху справа - вниз слева
        if progress > 0.5:
            progress2 = (progress - 0.5) * 2.0
            start_x2, start_y2 = x + half_size, y - half_size  # Верхний правый
            end_x2, end_y2 = x - half_size, y + half_size  # Нижний левый
            current_x2 = start_x2 - (start_x2 - end_x2) * progress2
            current_y2 = start_y2 + (end_y2 - start_y2) * progress2
            
            self.canvas.create_line(
                start_x2, start_y2, current_x2, current_y2,
                fill="yellowgreen", width=4, capstyle="round",
                tags=f"symbol_{row}_{col}"
            )
        
    def animate_circle(self, row, col, progress):
        """Анимированная отрисовка нолика"""
        x, y = self.get_cell_center(row, col)
        
        # Размеры овала
        cell_width = self.cell_size
        cell_height = self.cell_size
        
        # Отступы
        padding_x = cell_width * 0.1
        padding_y = cell_height * 0.1
        
        # Ширина и высота овала
        oval_width = cell_width - 2 * padding_x
        oval_height = cell_height - 2 * padding_y
        
        # Прямоугольник, в который вписан овал
        x1 = x - oval_width / 2
        y1 = y - oval_height / 2
        x2 = x + oval_width / 2
        y2 = y + oval_height / 2
        
        # Начальный угол (в градусах)
        start_angle = 90
        
        # Конечный угол: зависит от прогресса
        extent = 360 * min(progress, 0.99)  # Максимум 359 градусов
        
        # Рисуем дугу
        self.canvas.create_arc(
            x1, y1, x2, y2,
            start=start_angle,
            extent=extent,
            style=tk.ARC,
            outline="blue", width=4,
            tags=f"symbol_{row}_{col}"
        )
        
    def animate_winning_line(self):
        """Анимирует отрисовку победной линии"""
        if not self.winning_line:
            return
            
        # Находим начальную и конечную точки линии
        start_row, start_col = self.winning_line[0]
        end_row, end_col = self.winning_line[-1]
        
        # Получаем центры ячеек
        start_x, start_y = self.get_cell_center(start_row, start_col)
        end_x, end_y = self.get_cell_center(end_row, end_col)
        
        self.win_line_start = (start_x, start_y)
        self.win_line_end = (end_x, end_y)
        self.win_line_progress = 0.0
        
        # Удаляем старую линию, если она есть
        self.canvas.delete("win_line")
        
        self._animate_winning_line_step()
        
    def _animate_winning_line_step(self):
        """Вспомогательный метод для анимации победной линии"""
        if not self.win_line_start or not self.win_line_end:
            return
            
        start_x, start_y = self.win_line_start
        end_x, end_y = self.win_line_end
        
        # Увеличиваем прогресс
        self.win_line_progress += 0.03  # Скорость анимации линии
        self.win_line_progress = min(self.win_line_progress, 1.0)
        
        # Рассчитываем текущую конечную точку линии
        current_x = start_x + (end_x - start_x) * self.win_line_progress
        current_y = start_y + (end_y - start_y) * self.win_line_progress
        
        # Удаляем предыдущую линию
        self.canvas.delete("win_line")
        
        # Рисуем новую линию
        self.canvas.create_line(
            start_x, start_y, current_x, current_y,
            fill="red", width=6, capstyle="round",
            tags="win_line"
        )
        
        # Продолжаем анимацию
        if self.win_line_progress < 1.0:
            self.root.after(50, self._animate_winning_line_step)
        else:
            # Анимация завершена, показываем сообщение о победе
            winner = self.board.get_cell(self.winning_line[0][0], self.winning_line[0][1])
            self.root.after(100, lambda: messagebox.showinfo("Победа!", f"Игрок {winner} победил!"))
        
    def start_new_game(self):
        """Запускает новую игру"""
        # Сбрасываем всю логику игры к начальному состоянию
        self.game.reset()
        
        # Обновляем ссылки на объекты
        self.board = self.game.board
        
        # Сбрасываем анимации
        self.animations.clear()
        
        # Очищаем холст от всех игровых элементов
        self.canvas.delete("symbol")
        self.canvas.delete("win_line")
        # Удаляем все крестики и нолики
        self.canvas.delete("all")
        self.draw_grid()
        
        # Сбрасываем состояние анимации победной линии
        self.win_line_start = None
        self.win_line_end = None
        self.win_line_progress = 0.0
        self.winning_line = []
        
        # Сбрасываем состояние игры
        self.game_active = True
        
        # Перерисовываем сетку
        self.draw_grid()