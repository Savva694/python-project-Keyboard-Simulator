# Keyboard Simulator

import sys
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout

# Создание json с пустой статистикой
stats = {"Пройдено уровней": 0,
         "Вероятность ошибки": 0,
         "Количество введённых символов": 0,
         "Количество ошибок": 0,
         "Наиболее частые ошибки": 0,
         "Ср. время набора символа": 0,
         "Затрачено времени в сумме": 0}
for i in range(32):
    stats["Ошибок на букве " + chr(ord("а") + i)] = 0
    stats["Верных нажатий на букве " + chr(ord("а") + i)] = 0
    stats["Ошибок на букве " + chr(ord("А") + i)] = 0
    stats["Верных нажатий на букве " + chr(ord("А") + i)] = 0
with open('STATS.txt', 'w') as outfile:
    json.dump(stats, outfile)


# Класс для перехвата вводимых символов
class CustomLineEdit(QLineEdit):
    def __init__(self, level_text, parent=None):
        super(CustomLineEdit, self).__init__(parent)
        self.level_text = level_text
        self.now_position = 0
        self.end_position = len(level_text)

    def keyPressEvent(self, event):
        if self.now_position != self.end_position:
            key = event.key()
            print(key, chr(key))
            if chr(key) == (self.level_text[self.now_position]).title():
                self.now_position += 1
                super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        # Объявление переменных для визуала
        self.btn_sep = 10

        self.btn_levels_width = 100
        self.btn_levels_height = 50

        self.levels_count = 10
        self.btn_level_width = 70
        self.btn_level_height = 50
        self.btn_level_start_height = self.btn_sep * 2 + self.btn_levels_height
        self.btn_level_in_row_count = 4

        self.btn_stats_width = 100
        self.btn_stats_height = 50
        self.btn_stats_start_width = self.btn_sep * 3 + (
                self.btn_sep + self.btn_level_width) * self.btn_level_in_row_count
        self.btn_stats_start_height = self.btn_sep

        self.text_stats_width = 300
        self.text_stats_height = 100
        self.text_stats_start_width = self.btn_stats_start_width
        self.text_stats_start_height = self.btn_stats_start_height + self.btn_stats_height + self.btn_sep

        self.btn_start_level_width = 100
        self.btn_start_level_height = 50
        self.btn_start_level_start_width = self.btn_sep
        self.btn_start_level_start_height = self.btn_level_start_height + self.btn_sep * 2 + (
                self.btn_sep + self.btn_level_height) * ((
                                                                 self.levels_count + self.btn_level_in_row_count - 1) // self.btn_level_in_row_count)

        self.btn_finish_level_width = 100
        self.btn_finish_level_height = 50
        self.btn_finish_level_start_width = self.btn_sep * 4 + self.btn_start_level_width
        self.btn_finish_level_start_height = self.btn_level_start_height + self.btn_sep * 2 + (
                self.btn_sep + self.btn_level_height) * ((
                                                                 self.levels_count + self.btn_level_in_row_count - 1) // self.btn_level_in_row_count)

        # Отрисовка главного окна и его виджетов
        super(MainWindow, self).__init__()

        self.setWindowTitle("Keyboard Simulator")
        self.setGeometry(650, 250, 600, 600)
        self.show()

        # Кнопка показа уровней
        self.btn_levels = QPushButton("Show Levels", self)
        self.btn_levels.resize(self.btn_levels_width, self.btn_levels_height)
        self.btn_levels.move(self.btn_sep, self.btn_sep)
        self.btn_levels.clicked.connect(self.show_or_hide_levels)
        self.btn_levels.show()

        # Кнопки уровней
        self.levels = list()
        for i in range(self.levels_count):
            self.levels.append(QPushButton("Level " + str(i + 1), self))
            self.levels[-1].resize(self.btn_level_width, self.btn_level_height)
            self.levels[-1].move(-1000, -1000)
            self.levels[-1].clicked.connect(self.view_level)
            self.levels[-1].show()

        # Кнопка показа статистики
        self.btn_stats = QPushButton("Show Stats", self)
        self.btn_stats.resize(self.btn_stats_width, self.btn_stats_height)
        self.btn_stats.move(self.btn_stats_start_width, self.btn_stats_start_height)
        self.btn_stats.clicked.connect(self.show_or_hide_stats)
        self.btn_stats.show()

        # Чтение статистики из json файла
        with open('STATS.txt') as json_stats:
            self.stats = json.load(json_stats)
        # for i in self.stats.keys():
        #     print(i + " " + str(self.stats[i]))

        self.text_stats = QLabel("none", self)
        self.text_stats.setText("Пройдено уровней:  " + str(self.stats["Пройдено уровней"]) + "\n")
        self.text_stats.setText(
            self.text_stats.text() + "Вероятность ошибки:  " + str(self.stats["Вероятность ошибки"]) + "\n")
        self.text_stats.setText(
            self.text_stats.text() + "Наиболее частые ошибки:  " + str(self.stats["Наиболее частые ошибки"]) + "\n")
        self.text_stats.setText(
            self.text_stats.text() + "Ср. время набора символа:  " + str(self.stats["Ср. время набора символа"]) + "\n")

        self.text_stats.resize(self.text_stats_width, self.text_stats_height)
        self.text_stats.move(-1000, -1000)
        self.text_stats.show()

        # Кнопка старта уровня
        self.btn_start_level = QPushButton("Start Level", self)
        self.btn_start_level.resize(self.btn_start_level_width, self.btn_start_level_height)
        self.btn_start_level.move(self.btn_start_level_start_width, self.btn_start_level_start_height)
        self.btn_start_level.clicked.connect(self.start_level)
        self.btn_start_level.show()

        # Кнопка окончания уровня
        self.btn_finish_level = QPushButton("Finish Level", self)
        self.btn_finish_level.resize(self.btn_finish_level_width, self.btn_finish_level_height)
        self.btn_finish_level.move(self.btn_finish_level_start_width, self.btn_finish_level_start_height)
        self.btn_finish_level.clicked.connect(self.finish_level)
        self.btn_finish_level.show()

        # Поле ввода
        self.input_text = CustomLineEdit("aboba", self)
        self.input_text.resize(500, 100)
        self.input_text.move(self.btn_finish_level_start_width, self.btn_finish_level_start_height)
        self.input_text.show()

    def show_or_hide_levels(self):
        if self.btn_levels.text() == "Show Levels":
            self.btn_levels.setText("Hide Levels")

            for i in range(self.levels_count):
                self.levels[i].move(
                    self.btn_sep + (self.btn_sep + self.btn_level_width) * (i % self.btn_level_in_row_count),
                    self.btn_level_start_height + (
                            self.btn_sep + self.btn_level_height) * (i // self.btn_level_in_row_count))
        else:
            self.btn_levels.setText("Show Levels")

            for i in range(self.levels_count):
                self.levels[i].move(-1000, -1000)

    def view_level(self):
        button = QApplication.instance().sender()
        lvl_number = int(button.text().split()[-1])
        print(lvl_number)

    def show_or_hide_stats(self):
        if self.btn_stats.text() == "Show Stats":
            self.btn_stats.setText("Hide Stats")
            self.text_stats.move(self.text_stats_start_width, self.text_stats_start_height)
        else:
            self.btn_stats.setText("Show Stats")
            self.text_stats.move(-1000, -1000)

    def start_level(self):
        print("Level started")

    def finish_level(self):
        print("Level finished")


app = QApplication(sys.argv)
window = MainWindow()

app.exec()
