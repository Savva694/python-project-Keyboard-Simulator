from PyQt5.QtWidgets import QLineEdit


# Класс для перехвата вводимых символов
class CustomLineEdit(QLineEdit):
    def __init__(self, level_info, parent=None):
        super(CustomLineEdit, self).__init__(parent)
        self.level_info = level_info

    def update_stats(self, key, correct=True):
        self.level_info[4]["Количество ошибок" if not correct else "Количество введённых символов"] += 1
        if ord("А") <= key <= ord("Я") or ord("A") <= key <= ord("Z"):
            key_char = chr(key)
            if correct:
                stat_key = f"Верных нажатий на букве {key_char}"
            else:
                stat_key = f"Ошибок на букве {key_char}"
            self.level_info[4][stat_key] += 1

    def keyPressEvent(self, event):
        if (not self.level_info[3]):
            return
        if self.level_info[0] != len(self.level_info[1]):
            key = event.key()
            MAX_ORD = 1114111
            if not (0 <= key <= MAX_ORD):
                return

            if chr(key) == (self.level_info[1][self.level_info[0]]).title():
                self.update_stats(key, True)
                self.level_info[0] += 1
                if self.level_info[0] < 25:
                    self.level_info[2].setText(
                        (self.level_info[1] + 50 * " ")[0:self.level_info[0] + 50])
                else:
                    self.level_info[2].setText(
                        (self.level_info[1] + 50 * " ")[self.level_info[0] - 24:self.level_info[0] + 26])
                super().keyPressEvent(event)
            else:
                self.update_stats(key, False)
