## Keyboard Simulator
# Автор: Чуев Савва, Б05-327
# Описание проекта и реализуемый функционал
Проект предназначен для тренировки набора текста на клавиатуре.
Изначально пользователю доступно 10 встроенных уровней с набором текста. Эти уровни сгенерированы мной.
Также пользователю доступна общая статистика его прохождения уровней. В статистике указываются такие величины, как: количество пройденных уровней; вероятность ошибки в процентах; символы, на которых пользователь ошибается чаще всего; среднее время, затрачиваемое на набор одного символа и т.д. Статистика сохранятся после закрытия приложения. Статистику можно сбросить.

# Архитектура проекта
Проект будет использовать такую библиотеку, как PyQt5.
Будет создан класс MainWindow, наследующийся от QMainWindow - окно с главым интерфейсом. В качестве полей он будет содержать виджеты этого окна: кнопки, тестовые виджеты и т.д. Также у этого класа будут методы, к которым привязаны кнопки, например: show_or_hide_levels - метод, открывающий или закрывающий доступ к уровням, show_or_hide_stats - метод, открывающий или закрывающий доступ к статистике, start_level - метод, вызывающийся при запуске какого-либо уровня и т.д.
Статистика будет храниться в json формате в виде словаря и автоматически обновляться при прохождении уровня.

# Планируемые улучшения
1) Добавить больше встроенных уроней.
2) Разделить уровни на 3 категории:
    2.1) Уровни для обучения (в них отрабатывается ограниченный набор символов)
    2.2) Уровни для тренировки (в них присутствует большой набор различных символов, они представляют собой обычный текст)
    2.3) Другое (уровни для тренировки английского языка или уровни для тренировки команд на python, c++ и т.д.)
3) Добавить возможность пользователю загружать свои уровни в формате текстовых файлов.
4) Добавить больше разнообразной статистики.
