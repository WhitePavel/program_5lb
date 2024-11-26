from bs4 import BeautifulSoup
import json
import re
with open("index.html") as file:
    src = file.read()

soup = BeautifulSoup(src,"lxml")

celler_data = soup.find("tr",onclick=True).find_all(["a","div"],title=True)
dict_data_celler = {
    "Name":celler_data[0].text,
    "Checks":celler_data[1].text.replace("\xa0"," "),
    "Revenue":celler_data[3].text.replace("\xa0"," "),
    "Margin":celler_data[11].text.replace("\xa0"," ")

}
print(dict_data_celler)

with open("name.json","w") as file:
    json.dump(dict_data_celler,file,indent=4,ensure_ascii=False)

