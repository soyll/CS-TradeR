# console.py
# управляет выводом, возвращает стилизованный текст с гибкой настройкой
# made by soylir

import os
from colorama import init, Fore, Back, Style
from datetime import datetime

class Console:
    def __init__(self):
        init()  # Инициализация colorama для поддержки цветов в консоли
        self.log_folder = "logs"

        self.previous_log = None
        self.log_count = 1

        # Создание папки для логов, если ее нет
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

    def printc(self, text, bg_color=None, fg_color=None, style=None):
        style_str = ""

        # Установка стиля
        if style == "bold":
            style_str += Style.BRIGHT
        elif style == "italic":
            style_str += Style.DIM

        # Установка цвета фона
        if bg_color:
            bg_color_str = getattr(Back, bg_color.upper(), "")
            style_str += bg_color_str

        # Установка цвета текста
        if fg_color:
            fg_color_str = getattr(Fore, fg_color.upper(), "")
            style_str += fg_color_str

        # Получаем текущее время
        current_time = datetime.now().strftime("%H:%M:%S")

        # Вывод текста с установленными стилем, цветом текста и фоном
        print(style_str + f"{current_time} --> {text}" + Style.RESET_ALL)

    def log(self, text, log_level="INFO", print_to=True):
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d-%m")
        current_hour = datetime.now().hour // 6

        caller_file = os.path.basename(__file__)[:-3]
        log_file_name = os.path.join(self.log_folder, f"{caller_file}_{current_date}_{current_hour}.log")

        log_string = f"{current_time} --> {log_level}: {text}"  # Вставляем информацию о контексте в начало строки

        if print_to:
            style = ""
            if log_level == "ERROR":
                style = Fore.RED
            elif log_level == "INFO":
                style = Fore.YELLOW
            print(style + log_string + Style.RESET_ALL)

        with open(log_file_name, 'a') as file:
            if self.previous_log == log_string:
                self.log_count += 1
                if self.log_count == 2:
                    file.write(f"({self.log_count})\n")
            else:
                if self.previous_log is not None and self.log_count > 1:
                    file.write(f"({self.log_count})\n")
                file.write(log_string + '\n')
                self.log_count = 1
            self.previous_log = log_string