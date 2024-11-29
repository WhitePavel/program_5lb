import os
import time
import datetime
import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait            # import for wait
from selenium.webdriver.support import expected_conditions as EC   # import for wait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--******")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=chrome_options)
wait = WebDriverWait(driver,20,poll_frequency=15)   # время ожидания и интервал запросов

with open("/Users/pavelprosvetov/my_sklad_key.json") as file_json:
    key_my_sklad = json.load(file_json)

driver.get('https://www.moysklad.ru/login/')

login_field= ("xpath","//input[@name='j_username']")
password_field = ("xpath","//input[@name='j_password']")
entry_button = ("xpath","//button[@type='submit']")

workers = ("xpath","//span[text()='По сотрудникам']")
current_data = datetime.datetime.now().strftime('%d.%m.%Y')

wait.until(EC.element_to_be_clickable(login_field)).send_keys(key_my_sklad["Login"])
wait.until(EC.element_to_be_clickable(password_field)).send_keys(key_my_sklad["Key"])
wait.until(EC.element_to_be_clickable(entry_button)).click()

driver.get(f"https://online.moysklad.ru/app/#pnl?periodFilter={current_data}%2000:00:00,{current_data}%2023:59:00,inside_period&global_retailStoreFilter=%5B4ebadb98-ece1-11ee-0a80-010a000b7214%5C%5C,Ашан%20Рязанка%5C%5C,%5C%5C,RetailStore%5D,equals&sort=goodName%20a")
wait.until(EC.element_to_be_clickable(workers)).click()
time.sleep(5)

src = driver.page_source
with open("dependencies/index.html","w") as file:
    file.write(src)