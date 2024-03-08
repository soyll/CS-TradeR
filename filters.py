# filters.py
# управляет фильтрами для таблицы, возвращает фильтры в dict
# made by soylir

import os.path
import json
import asyncio

# Ключи для фильтров
keys = [
    "MIN_PERCENT",
    "MAX_PERCENT",
    "MIN_PRICE",
    "MAX_PRICE",
    "MIN_COUNT",
    "APP_NUM",
    "SECOND_SERVICE",
    "STEAM_SALES_NUM",
    "CSTRADE_SALES_NUM",
    "AUTO_BUY"
]

class Filter:
    def __init__(self):
        # Инициализация объекта
        self.log_folder = "logs"

        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

    async def get_filters(self):
        # Загрузка фильтров из файла
        filters = {}
        if os.path.isfile("filters.json"):
            try:
                with open("filters.json", "r") as file:
                    filters = json.load(file)
            except Exception as e:
                print(f"Ошибка при загрузке фильтров: {e}")
        else:
            print("Файл filters.json не найден.")

        return filters

    async def set_filters(self):
        # Установка фильтров пользователем
        filters = {}
        for key in keys:
            try:
                user_input = await self.get_user_input(key)
                new_value = int(user_input) if user_input else ""
                filters[key] = new_value
            except ValueError as e:
                print(f"{e}\nНеправильно введенное значение.")
                break
            
        else:
            # Запись фильтров в файл
            try:
                with open("filters.json", "w") as file:
                    json.dump(filters, file, indent=4)
            except Exception as e:
                print(f"Ошибка при записи фильтров: {e}")

        return filters

    async def get_user_input(self, key):
        # Получение ввода пользователя с учетом разных типов данных
        translation = self.translate(key)
        user_input = input(f"{translation}: ")
        return user_input.strip()

    async def is_valid_filters(self, filters_data):
        # Проверка валидности фильтров
        required_keys = ["MIN_PERCENT", "MAX_PERCENT", "MIN_PRICE", "MAX_PRICE", "MIN_COUNT", "APP_NUM", "SECOND_SERVICE", "STEAM_SALES_NUM", "CSTRADE_SALES_NUM", "AUTO_BUY"]
        return all(key in filters_data and filters_data[key] is not None for key in required_keys)

    def translate(self, string):
        # Перевод ключей фильтров на человеческий язык
        translations = {
            "MIN_PERCENT": "Введите минимальный процент прибыли",
            "MAX_PERCENT": "Введите максимальный процент прибыли",
            "MIN_PRICE": "Введите минимальную цену",
            "MAX_PRICE": "Введите максимальную цену",
            "MIN_COUNT": "Введите минимальное количество",
            "APP_NUM": "Введите номер игры (1: Все; 2: CS; 3: Dota 2; 4: Rust; 5: ;)",
            "SECOND_SERVICE": "Введите второй сервис для сравнения (1: Steam; 2: TM Market;)",
            "STEAM_SALES_NUM": "Введите количество продаж в Steam",
            "CSTRADE_SALES_NUM": "Введите количество продаж в CS.TRADE",
            "AUTO_BUY": "Введите параметр для автобая (1, 2)"
        }
        return translations.get(string, "")

    async def convert_filters_to_url(self, filters_data):
        # Конвертация фильтров в URL
        app_values = {
            1: "all",
            2: 2,
            3: 3,
            4: 5,
            5: 7
        }
        app = app_values.get(filters_data.get("APP_NUM"), "all")
        
        services = ["cs.trade"]
        if filters_data.get("SECOND_SERVICE") == 1:
            services.append("steamcommunity.com")
        elif filters_data.get("SECOND_SERVICE") == 2:
            services.append("tm_market")
        
        price = [[filters_data.get("MIN_PRICE", ""), filters_data.get("MAX_PRICE", "")]]
        
        count = [[filters_data.get("MIN_COUNT", "")], []]
        
        profit = [[filters_data.get("MIN_PERCENT", ""), filters_data.get("MAX_PERCENT", "")]]
        
        arguments = {
            "app": app,
            "services": services,
            "price": price,
            "count": count,
            "profit": profit
        }
        
        link = "https://tradeback.io/ru/comparison#" + json.dumps(arguments, separators=(',', ':'))
        
        return link