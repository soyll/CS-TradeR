# _trader.py
# управляет всеми покупками, возвращает True в случае покупки, иначе ошибку
# made by soylir

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import asyncio
import inspect

import console
import _parser

class Trader:
    def __init__(self, cookie_value, titles, prices):
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://cs.trade/trade")
        self.driver.add_cookie({"name": "PHPSESSID", "value": cookie_value["PHPSESSID"][0]})
        self.driver.refresh()
        self.titles = titles
        self.prices = prices
        self.step = 2
        self.buy_skin = []
        self.buy_sum = []
        

    async def buy(self):
        c = console.Console()
        c.printc("Инвентарь загружается...", "black", "gray", "italic")
        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#box-bot-inventory .inventory-bot-preloader'))
                )
            except:
                c.printc("Инвентарь загружен", "black", "green", "bold")
                c.log("Inventory Pass", "INFO", print_to=False)
                
                for title, price in zip(self.titles, self.prices):
                    try:
                        bot_search_input = self.driver.find_element(By.ID, 'bot_search')
                        bot_search_input.clear()
                        bot_search_input.send_keys(title)

                        item_box = self.driver.find_element(By.XPATH, '//*[@id="box-bot-inventory"]')
                        items = item_box.find_elements(By.CLASS_NAME, 'single-item')
                        
                        for item in items:
                            try:
                                item_id = item.get_property("id")
                                item_xpath = '//*[@id="{}"]/small[2]'.format(item_id)
                                item_price = float(str(item.find_element(By.XPATH, item_xpath).text)[1:])
                                if price - self.step <= item_price <= price + self.step:
                                    item.click()
                                    self.driver.execute_script("trade()")
                                    self.driver.execute_script("clearTradesQueue()")
                                    alert = self.driver.switch_to.alert
                                    alert.accept()
                                    self.buy_skin.append(title)
                                    self.buy_sum.append("$" + str(price))
                                    break
                            except:
                                if self.close_windows():
                                    pass
                                else:
                                    break
                    except Exception as e:
                        c.log(f"{inspect.getframeinfo(inspect.currentframe()).filename} | {e.__class__.__name__}: {e}", "ERROR")
                        return str(e.__class__.__name__)
                if self.buy_skin != [] and self.buy_sum != []:
                    self.balance = await _parser.Parse().get_balance()
                    return self.buy_skin, self.buy_sum, self.balance


        self.driver.quit()
        return self.buy_skin, self.buy_sum

    def close_windows(self):
        # Обработка возможных всплывающих окон
        try:
            accept_button = self.driver.find_element(By.XPATH, '//*[@id="iubenda-cs-banner"]/div/div/div/div[4]/div[2]/button[2]')
            accept_button.click()
        except Exception as e:
            pass

        try:
            dialog_count = self.driver.find_element(By.XPATH, '//*[@id="dialog-bw-count"]/span')
            dialog_count.click()
        except Exception as e:
            pass

        try:
            ui_button = self.driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/button')
            ui_button.click()
        except Exception as e:
            pass