# controller.py
# управляет всеми скриптами, является головным скриптом
# made by soylir

import asyncio
import _parser
import _trader
import console
from cookies import get_cookies
import json

console = console.Console()

cookie = get_cookies()

error_list = ["ElementNotInteractableException", "ValueError", "TypeError"]

async def run():
    trader_result = ""
    while True: 
        if trader_result not in error_list:            
            # Получаем текущий баланс
            balance = await _parser.Parse().get_balance()
            
            # Выполняем функцию парсера
            s, p = await _parser.Parse().parse_table()

            # Если парсер вернул False, прерываем цикл
            if not s and not p:
                console.log('_Parser вернул ошибку. Перезапускаем цикл', log_level="INFO")
                break

            # Выполняем функцию трейдера
            trader_result = await _trader.Trader(cookie[2], s, p).buy()
            
            try:
                if trader_result[0] != [] and trader_result[1] != []:
                    console.log(f"Buyed: {trader_result[0]} \n {trader_result[1]} \n old-balance: {balance} new-balance: {trader_result[2]}", log_level="DEBUG", print_to=False)
                    console.printc(f"Куплено: {len(trader_result[0])} шт. Баланс: ${float(trader_result[2])}", "black", "green", "italic") 
            except Exception as e: 
                console.log(e, log_level="ERROR")
            
        elif trader_result == "TypeError" or "AttributeError":
            # Ошибка. Выход из кода.
            console.printc("Ошибка. Перезапустите скрипт или обратитесь к разработчику.", "black", "red", "bold")
            console.log(f'Critical Error: {trader_result}', log_level="ERROR")
            exit()
            
        elif trader_result == error_list[0]:
            # Выполняем функцию трейдера
            
            console.log(f'{trader_result}', log_level="INFO")
            
            trader_result = await _trader.Trader(cookie[2], s, p).buy()
if __name__ == "__main__":
    asyncio.run(run())