import json
import time

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from src.custom_line_edit import CustomLineEdit


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
                self.btn_sep + self.btn_level_height) * ((self.levels_count + self.btn_level_in_row_count - 1) //
                                                         self.btn_level_in_row_count)

        self.btn_finish_level_width = 100
        self.btn_finish_level_height = 50
        self.btn_finish_level_start_width = self.btn_sep * 4 + self.btn_start_level_width
        self.btn_finish_level_start_height = self.btn_level_start_height + self.btn_sep * 2 + (
                self.btn_sep + self.btn_level_height) * ((self.levels_count + self.btn_level_in_row_count - 1) //
                                                         self.btn_level_in_row_count)

        self.level_text_width = 400
        self.level_text_height = 25
        self.level_text_start_width = self.btn_sep + 7
        self.level_text_start_height = (self.btn_finish_level_start_height + self.btn_finish_level_height +
                                        self.btn_sep)

        self.line_edit_input_text_width = 190
        self.line_edit_input_text_height = 25
        self.line_edit_input_text_start_width = self.level_text_start_width
        self.line_edit_input_text_start_height = (self.level_text_start_height + self.level_text_height)

        self.cle_values = [0, 0, 0, False, 0]

        self.now_level_number = 0
        self.now_time = 0

        # Отрисовка главного окна и его виджетов
        super(MainWindow, self).__init__()

        self.setWindowTitle("Keyboard Simulator")
        self.setGeometry(650, 250, 610, 600)
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
        self.btn_stats = QPushButton("Update Stats", self)
        self.btn_stats.resize(self.btn_stats_width, self.btn_stats_height)
        self.btn_stats.move(self.btn_stats_start_width, self.btn_stats_start_height)
        self.btn_stats.clicked.connect(self.update_stats)
        self.btn_stats.show()

        # Кнопка сброса статистики
        self.btn_reset_stats = QPushButton("Reset Stats", self)
        self.btn_reset_stats.resize(self.btn_stats_width, self.btn_stats_height)
        self.btn_reset_stats.move(self.btn_stats_start_width + self.btn_stats_width + self.btn_sep,
                                  self.btn_stats_start_height)
        self.btn_reset_stats.clicked.connect(self.reset_stats)
        self.btn_reset_stats.show()

        # Чтение статистики из json файла
        with open('src/stats.txt') as json_stats:
            self.cle_values[4] = json.load(json_stats)

        self.text_stats = QLabel("none", self)
        self.update_stats()

        self.text_stats.resize(self.text_stats_width, self.text_stats_height)
        self.text_stats.move(self.text_stats_start_width, self.text_stats_start_height)
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

        # Текст уровня
        self.cle_values[2] = QLabel("none", self)
        self.cle_values[2].setText("Тут должен быть текст уровня...")
        self.cle_values[2].resize(self.level_text_width, self.level_text_height)
        self.cle_values[2].move(-1000, -1000)
        self.cle_values[2].show()

        # Поле ввода
        self.input_text = CustomLineEdit(self.cle_values, self)
        self.input_text.resize(self.line_edit_input_text_width, self.line_edit_input_text_height)
        self.input_text.move(-1000, -1000)
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
        self.now_level_number = button.text().split()[-1]
        self.cle_values[0] = 0
        self.cle_values[2].move(self.level_text_start_width, self.level_text_start_height)
        self.input_text.move(self.line_edit_input_text_start_width, self.line_edit_input_text_start_height)

        filename = "src/LEVELS/LEVEL_" + self.now_level_number + ".txt"
        with open(filename, "r") as file:
            self.cle_values[1] = file.read()
        self.cle_values[2].setText(
            (self.cle_values[1] + 50 * " ")[0:self.cle_values[0] + 100])

    def update_stats(self):
        self.text_stats.setText("Пройдено уровней:  " + str(self.cle_values[4]["Пройдено уровней"]) + "\n")
        self.text_stats.setText(
            self.text_stats.text() + "Вероятность ошибки:  " + str(
                int(self.cle_values[4]["Вероятность ошибки"])) + "%\n")
        self.text_stats.setText(
            self.text_stats.text() + "Наиболее частые ошибки:  " + str(
                self.cle_values[4]["Наиболее частые ошибки"]) + "\n")
        self.text_stats.setText(
            self.text_stats.text() + "Ср. время набора символа:  " + str(
                round(self.cle_values[4]["Ср. время набора символа"], 2)) + " c.\n")

        with open('src/stats.txt', 'w') as outfile:
            json.dump(self.cle_values[4], outfile)

    def reset_stats(self):
        stats = {"Пройдено уровней": 0,
                 "Вероятность ошибки": 0,
                 "Наиболее частые ошибки": "-",
                 "Ср. время набора символа": 0,
                 "Количество введённых символов": 1,
                 "Количество ошибок": 0,
                 "Затрачено времени в сумме": 0}

        for i in range(32):
            stats["Ошибок на букве " + chr(ord("А") + i)] = 0
            stats["Верных нажатий на букве " + chr(ord("А") + i)] = 0

        for i in range(ord("Z") - ord("A")):
            stats["Ошибок на букве " + chr(ord("A") + i)] = 0
            stats["Верных нажатий на букве " + chr(ord("A") + i)] = 0

        with open('src/stats.txt', 'w') as outfile:
            json.dump(stats, outfile)

        with open('src/stats.txt') as json_stats:
            self.cle_values[4] = json.load(json_stats)

        self.update_stats()

    def start_level(self):
        if int(self.now_level_number) < 1 or int(self.now_level_number) > self.levels_count:
            return
        self.cle_values[3] = True
        self.now_time = time.time()

    def finish_level(self):
        self.now_time = time.time() - self.now_time
        self.cle_values[0] = 0
        self.cle_values[2].move(-1000, -1000)
        self.cle_values[3] = False

        if self.cle_values[0] == len(self.cle_values[1]):
            self.cle_values[4]["Пройдено уровней"] += 1
        self.cle_values[4]["Затрачено времени в сумме"] += self.now_time
        self.cle_values[4]["Ср. время набора символа"] = (self.cle_values[4]["Затрачено времени в сумме"] /
                                                          self.cle_values[4]["Количество введённых символов"])
        self.cle_values[4]["Вероятность ошибки"] = (self.cle_values[4]["Количество ошибок"] /
                                                    (self.cle_values[4]["Количество введённых символов"] +
                                                     self.cle_values[4]["Количество ошибок"] + 1)) * 100

        best_mistakes = ["-", -1]
        for i in range(32):
            mistakes = self.cle_values[4]["Ошибок на букве " + chr(ord("А") + i)] / (
                    self.cle_values[4]["Ошибок на букве " + chr(ord("А") + i)] + self.cle_values[4][
                "Верных нажатий на букве " + chr(ord("А") + i)] + 1)
            if (mistakes > best_mistakes[1]):
                best_mistakes = [chr(ord("А") + i) + " (ru)", mistakes]

        for i in range(ord("Z") - ord("A")):
            mistakes = self.cle_values[4]["Ошибок на букве " + chr(ord("A") + i)] / (
                    self.cle_values[4]["Ошибок на букве " + chr(ord("A") + i)] + self.cle_values[4][
                "Верных нажатий на букве " + chr(ord("A") + i)] + 1)
            if (mistakes > best_mistakes[1]):
                best_mistakes = [chr(ord("A") + i) + " (en)", mistakes]

        if best_mistakes[1] != 0:
            self.cle_values[4]["Наиболее частые ошибки"] = best_mistakes[0]

        self.input_text.setText("")
        self.input_text.move(-1000, -1000)
        self.now_level_number = 0
