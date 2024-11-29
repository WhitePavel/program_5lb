import gspread
import datetime
import json
gc = gspread.service_account(filename="dependencies/cred.json")
sh = gc.open_by_key('10Nf1CQChZLtu4zLXWrDqEwNEEZmOivhRkbjD51T6H7k')
wks = sh.worksheet("Лист1")
with open("dependencies/name.json") as file:
    src = json.load(file)

current_date = datetime.datetime.now().strftime('%d')

wks.update_cell(5+int(current_date),4, src["Name"])    # Имя
wks.update_cell(5+int(current_date),5,src["Revenue"])   # выручка ТО
wks.update_cell(5+int(current_date),6,src["Checks"])    # количество чеков
wks.update_cell(5+int(current_date),8,src["Margin"])    # Маржинальность
