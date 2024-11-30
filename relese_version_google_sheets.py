import time
import datetime
import json

from bs4 import BeautifulSoup

import gspread

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait            # import for wait
from selenium.webdriver.support import expected_conditions as EC   # import for wait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")                            # оция подстановки юзер агента(данный агент нужно найти)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=chrome_options)
wait = WebDriverWait(driver,25,poll_frequency=5)            # время ожидания и интервал запросов

with open("dependencies/my_sklad_key.json") as file_json:  # получение логина и пароля с json файлов
    key_my_sklad = json.load(file_json)

driver.get('https://www.moysklad.ru/login/')

login_field= ("xpath","//input[@name='j_username']")
password_field = ("xpath","//input[@name='j_password']")             # поля на стартовой странице
entry_button = ("xpath","//button[@type='submit']")

workers = ("xpath","//span[text()='По сотрудникам']")                # поля на открытие и дата сегодняешнего дня в нужном формате
current_data = datetime.datetime.now().strftime('%d.%m.%Y')

wait.until(EC.element_to_be_clickable(login_field)).send_keys(key_my_sklad["Login"])
wait.until(EC.element_to_be_clickable(password_field)).send_keys(key_my_sklad["Key"])   # входим в аккаунт
wait.until(EC.element_to_be_clickable(entry_button)).click()

driver.implicitly_wait(2)

driver.get(f"https://online.moysklad.ru/app/#pnl?periodFilter={current_data}%2000:00:00,{current_data}%2023:59:00,inside_period&global_retailStoreFilter=%5B4ebadb98-ece1-11ee-0a80-010a000b7214%5C%5C,Ашан%20Рязанка%5C%5C,%5C%5C,RetailStore%5D,equals&sort=goodName%20a")
wait.until(EC.element_to_be_clickable(workers)).click()                                 # переходим на нужную страницу и выбираем по работникам

driver.implicitly_wait(5)
src = driver.page_source                                                                # получаем page_source
driver.close()
driver.quit()

soup = BeautifulSoup(src,"lxml")

try:
    celler_data = soup.find("tr",onclick=True).find_all(["a","div"],title=True)    # обрабатываем нужные столбцы данных
except Exception:
    celler_data = []

if bool(celler_data) == True:
    dict_data_celler = {
        "Name":celler_data[0].text,
        "Checks":celler_data[1].text.replace("\xa0"," "),
        "Revenue":celler_data[3].text.replace("\xa0"," "),
        "Margin":celler_data[11].text.replace("\xa0"," ")                          # создаём нужный список программы

    }
else:
    dict_data_celler = {
        "Name": "Продавец",
        "Checks": "0",
        "Revenue": "0",
        "Margin": "0"

    }

gc = gspread.service_account(filename="dependencies/cred.json")                                  # импортируем gspread для работы с гугл таблицой
sh = gc.open_by_key(key_my_sklad["gs_id"])                                                       # ключ таблицы
wks = sh.worksheet("Лист1")                                                                      # рабочий лист

current_date_for_gs = datetime.datetime.now().strftime('%d')

wks.update_cell(5+int(current_date_for_gs),4, dict_data_celler["Name"])     # Имя
wks.update_cell(5+int(current_date_for_gs),5,dict_data_celler["Revenue"])   # выручка ТО
wks.update_cell(5+int(current_date_for_gs),6,dict_data_celler["Checks"])    # количество чеков
wks.update_cell(5+int(current_date_for_gs),8,dict_data_celler["Margin"])    # Маржинальность



