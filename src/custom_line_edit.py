from PyQt5.QtWidgets import QLineEdit


# Класс для перехвата вводимых символов
class CustomLineEdit(QLineEdit):
    def __init__(self, level_info, parent=None):
        super(CustomLineEdit, self).__init__(parent)
        self.level_info = level_info

    def keyPressEvent(self, event):
        if (not self.level_info[3]):
            return
        if self.level_info[0] != len(self.level_info[1]):
            key = event.key()
            if not (0 <= key <= 1114111):
                return
            if chr(key) == (self.level_info[1][self.level_info[0]]).title():

                if ord("А") <= key <= ord("Я"):
                    self.level_info[4]["Верных нажатий на букве " + chr(key)] += 1
                if ord("A") <= key <= ord("Z"):
                    self.level_info[4]["Верных нажатий на букве " + chr(key)] += 1
                self.level_info[4]["Количество введённых символов"] += 1

                self.level_info[0] += 1
                if self.level_info[0] < 25:
                    self.level_info[2].setText(
                        (self.level_info[1] + 50 * " ")[0:self.level_info[0] + 50])
                else:
                    self.level_info[2].setText(
                        (self.level_info[1] + 50 * " ")[self.level_info[0] - 24:self.level_info[0] + 26])
                super().keyPressEvent(event)
            else:
                if ord("А") <= key <= ord("Я"):
                    self.level_info[4]["Количество ошибок"] += 1
                    self.level_info[4]["Ошибок на букве " + chr(key)] += 1
                if ord("A") <= key <= ord("Z"):
                    self.level_info[4]["Количество ошибок"] += 1
                    self.level_info[4]["Ошибок на букве " + chr(key)] += 1
