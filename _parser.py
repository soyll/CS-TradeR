# _parser.py
# управляет парсингом таблицы, возращает 2 списка (скины, цены) в случае успеха, иначе ошибку
# made by soylir

import asyncio
import json
import aiohttp
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import inspect
import time

from cookies import get_cookies
import filters
import console
    
class Parse:
    def __init__(self):
        self.cookie = get_cookies()
        self.__cstrade_url = "https://cs.trade"
        self.balance = None
        self.s = []
        self.p = []

    async def get_balance(self):
        return format(float(BeautifulSoup(requests.get(self.__cstrade_url, cookies=self.cookie[2]).text, features="lxml").find("span", {"class": "balance-value"}).text), ".2f")

    async def parse_table(self):
        await self.get_balance()
        self.filter = filters.Filter()
        self.filters = await self.filter.get_filters()
        self.__url = await self.filter.convert_filters_to_url(self.filters)
        self.s, self.p = await self.get_html(self.__url, self.cookie[3])
        return self.s, self.p

    async def get_html(self, url, cookies):
        c = console.Console()
        c.printc("Таблица загружается...", "black", "gray", "italic")
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get("https://tradeback.io/")
        driver.add_cookie(cookies)
        driver.get(url)
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.copy-name')))
            c.printc("Таблица загружена", "black", "green", "bold")
            c.log("Table Pass", log_level="INFO", print_to=False)
        except:
            c.printc("Таблица не загружена", "black", "red", "bold")
            c.log("Table Error", log_level="ERROR", print_to=False)
    
        time.sleep(5)
    
        table = driver.find_element(By.CSS_SELECTOR, 'tbody[id="table-body"]')\

        rows = table.find_elements(By.TAG_NAME, 'tr')
        
        titles = []
        prices = []

        for row in rows:
            if rows.index(row) < len(rows):
                try:
                    cells = row.find_elements(By.TAG_NAME, 'td')

                    for cell in cells:
                        class_value = cell.get_attribute('class')
                        if "copy-name" in class_value.split(" "):
                            if cell.text is not None:
                                titles.append(cell.text)
                        elif "field-price" in class_value.split(" "):
                            if cell.text is not None:
                                prices.append(cell.text)
                except Exception as e:
                    if str(e.__class__.__name__) == "StaleElementReferenceException":
                        c.log(f"{inspect.getframeinfo(inspect.currentframe()).filename}-{inspect.getframeinfo(inspect.currentframe()).lineno} | {e.__class__.__name__}", log_level="INFO")
                    else:
                        c.log(f"{inspect.getframeinfo(inspect.currentframe()).filename}-{inspect.getframeinfo(inspect.currentframe()).lineno} | {e.__class__.__name__}", log_level="ERROR")
                    continue

        # После завершения цикла выводим результат и закрываем драйвер
        prices = [float(x.split("\n")[0]) for x in prices]
        c.log(f"\n {titles} \n {prices}", log_level="DEBUG", print_to=False)
        driver.quit()
        return titles, prices
            