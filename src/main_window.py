import json
import os
import time

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from src.custom_line_edit import CustomLineEdit
import src.constants as constants


class MainWindow(QMainWindow):
    def __init__(self):
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
        self.create_button(self.btn_levels, constants.BTN_LEVELS_WIDTH,
                           constants.BTN_LEVELS_HEIGHT, constants.BTN_SEP,
                           constants.BTN_SEP, self.show_or_hide_levels)

        # Кнопки уровней
        self.levels = list()
        for i in range(constants.LEVELS_COUNT):
            self.levels.append(QPushButton("Level " + str(i + 1), self))
            self.create_button(self.levels[-1], constants.BTN_LEVEL_WIDTH,
                               constants.BTN_LEVEL_HEIGHT, -1000, -1000, self.view_level)

        # Кнопка показа статистики
        self.btn_stats = QPushButton("Update Stats", self)
        self.create_button(self.btn_stats, constants.BTN_STATS_WIDTH, constants.BTN_STATS_HEIGHT,
                           constants.BTN_STATS_START_WIDTH, constants.BTN_STATS_START_HEIGHT, self.update_stats)

        # Кнопка сброса статистики
        self.btn_reset_stats = QPushButton("Reset Stats", self)
        self.create_button(self.btn_reset_stats, constants.BTN_STATS_WIDTH, constants.BTN_STATS_HEIGHT,
                           constants.BTN_STATS_START_WIDTH + constants.BTN_STATS_WIDTH + constants.BTN_SEP,
                           constants.BTN_STATS_START_HEIGHT, self.reset_stats)

        # Чтение статистики из json файла
        with open(os.path.join("src", "stats.txt")) as json_stats:
            self.cle_values[4] = json.load(json_stats)

        self.text_stats = QLabel("none", self)
        self.update_stats()

        self.text_stats.resize(constants.TEXT_STATS_WIDTH, constants.TEXT_STATS_HEIGHT)
        self.text_stats.move(constants.TEXT_STATS_START_WIDTH, constants.TEXT_STATS_START_HEIGHT)
        self.text_stats.show()

        # Кнопка старта уровня
        self.btn_start_level = QPushButton("Start Level", self)
        self.create_button(self.btn_start_level, constants.BTN_START_LEVEL_WIDTH, constants.BTN_START_LEVEL_HEIGHT,
                           constants.BTN_START_LEVEL_START_WIDTH, constants.BTN_START_LEVEL_START_HEIGHT,
                           self.start_level)

        # Кнопка окончания уровня
        self.btn_finish_level = QPushButton("Finish Level", self)
        self.create_button(self.btn_finish_level, constants.BTN_FINISH_LEVEL_WIDTH, constants.BTN_FINISH_LEVEL_HEIGHT,
                           constants.BTN_FINISH_LEVEL_START_WIDTH, constants.BTN_FINISH_LEVEL_START_HEIGHT,
                           self.finish_level)

        # Текст уровня
        self.cle_values[2] = QLabel("none", self)
        self.cle_values[2].setText("Тут должен быть текст уровня...")
        self.cle_values[2].resize(constants.LEVEL_TEXT_WIDTH, constants.LEVEL_TEXT_HEIGHT)
        self.cle_values[2].move(-1000, -1000)
        self.cle_values[2].show()

        # Поле ввода
        self.input_text = CustomLineEdit(self.cle_values, self)
        self.input_text.resize(constants.LINE_EDIT_INPUT_TEXT_WIDTH, constants.LINE_EDIT_INPUT_TEXT_HEIGHT)
        self.input_text.move(-1000, -1000)
        self.input_text.show()

    def create_button(self, btn, width, height, start_width, start_height, function):
        btn.resize(width, height)
        btn.move(start_width, start_height)
        btn.clicked.connect(function)
        btn.show()

    def show_or_hide_levels(self):
        if self.btn_levels.text() == "Show Levels":
            self.btn_levels.setText("Hide Levels")

            for i in range(constants.LEVELS_COUNT):
                self.levels[i].move(
                    constants.BTN_SEP + (constants.BTN_SEP + constants.BTN_LEVEL_WIDTH) * (
                            i % constants.BTN_LEVEL_IN_ROW_COUNT),
                    constants.BTN_LEVEL_START_HEIGHT + (
                            constants.BTN_SEP + constants.BTN_LEVEL_HEIGHT) * (i // constants.BTN_LEVEL_IN_ROW_COUNT))
        else:
            self.btn_levels.setText("Show Levels")

            for i in range(constants.LEVELS_COUNT):
                self.levels[i].move(-1000, -1000)

    def view_level(self):
        button = QApplication.instance().sender()
        self.now_level_number = button.text().split()[-1]
        self.cle_values[0] = 0
        self.cle_values[2].move(constants.LEVEL_TEXT_START_WIDTH, constants.LEVEL_TEXT_START_HEIGHT)
        self.input_text.move(constants.LINE_EDIT_INPUT_TEXT_START_WIDTH, constants.LINE_EDIT_INPUT_TEXT_START_HEIGHT)

        filename = "src/LEVELS/LEVEL_" + self.now_level_number + ".txt"
        with open(filename, "r") as file:
            self.cle_values[1] = file.read()
        self.cle_values[2].setText(
            (self.cle_values[1] + 50 * " ")[0:self.cle_values[0] + 100])

    def update_stats(self):
        self.text_stats.setText("Пройдено уровней:  " + str(self.cle_values[4]["Пройдено уровней"]) + "\n"
                                + "Вероятность ошибки:  " + str(int(self.cle_values[4]["Вероятность ошибки"])) + "%\n"
                                + "Наиболее частые ошибки:  " + str(self.cle_values[4]["Наиболее частые ошибки"]) + "\n"
                                + "Ср. время набора символа:  " + str(
            round(self.cle_values[4]["Ср. время набора символа"], 2))
                                + " c.\n")

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

        with open(os.path.join("src", "stats.txt"), 'w') as outfile:
            json.dump(stats, outfile)

        with open(os.path.join("src", "stats.txt")) as json_stats:
            self.cle_values[4] = json.load(json_stats)

        self.update_stats()

    def start_level(self):
        if int(self.now_level_number) < 1 or int(self.now_level_number) > constants.LEVELS_COUNT:
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
        if int(self.cle_values[4]["Затрачено времени в сумме"] /
               (self.cle_values[4]["Количество введённых символов"] + 1)) < constants.MAX_TIME:
            self.cle_values[4]["Ср. время набора символа"] = (self.cle_values[4]["Затрачено времени в сумме"] /
                                                              (self.cle_values[4]["Количество введённых символов"] + 1))
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
        self.update_stats()
