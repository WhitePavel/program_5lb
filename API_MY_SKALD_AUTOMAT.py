from dotenv import load_dotenv
import os
import requests
import datetime
import json
import gspread

load_dotenv()
current_data = datetime.datetime.now().strftime('%Y-%m-%d')
payload = {}
headers = {
  'Authorization': os.getenv("API_KEY")
}


url = f"https://api.moysklad.ru/api/remap/1.2/report/profit/byemployee?filter=store=https://api.moysklad.ru/api/remap/1.2/entity/store/ce3b6c3b-ece0-11ee-0a80-16c4000b5fca&momentFrom={current_data} 00:00:00"

response = requests.request("GET", url, headers=headers, data=payload)

src=json.loads(response.text)

print(src["rows"][0]["employee"]["name"])
print((src["rows"][0]["salesCount"]))
print((src["rows"][0]["sellSum"])/100)
print((src["rows"][0]["profit"])/100)


gc = gspread.service_account(filename="dependencies/cred.json")                                  # импортируем gspread для работы с гугл таблицой
sh = gc.open_by_key(os.getenv("GS_TOKEN"))                                                       # ключ таблицы
wks = sh.worksheet("Рязанка Декабрь")                                                            # рабочий лист

current_date_for_gs = datetime.datetime.now().strftime('%d')

wks.update_cell(5+int(current_date_for_gs),4, src["rows"][0]["employee"]["name"])     # Имя
wks.update_cell(5+int(current_date_for_gs),5, (src["rows"][0]["sellSum"]/100))        # выручка ТО salesCount
wks.update_cell(5+int(current_date_for_gs),6, src["rows"][0]["salesCount"])           # количество чеков
wks.update_cell(5+int(current_date_for_gs),8, (src["rows"][0]["profit"]/100))        # Маржинальность
