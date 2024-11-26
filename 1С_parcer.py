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

with open("/Users/pavelprosvetov/1c_key.json") as file_json:
    key_my_sklad = json.load(file_json)

driver.get('https://services.5lb.ru/franch/ru_RU/')

login_button = ("xpath","//input[@id='userName']")
password_button = ("xpath","//input[@id='userPassword']")
ok_button = ("xpath","//button[@id='okButton']")

close_button = ("xpath","//span[@id='VW_page1headerTopLine_cmd_CloseButton']")
check_for_configuration = ("xpath","//span[text()='Ввести позже']")





wait.until(EC.element_to_be_clickable(login_button)).send_keys(key_my_sklad["User"])
wait.until(EC.element_to_be_clickable(password_button)).send_keys(key_my_sklad["Password"])
wait.until(EC.element_to_be_clickable(ok_button)).click()
wait.until(EC.element_to_be_clickable(close_button)).click()


