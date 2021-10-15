import requests
import json
from bs4 import BeautifulSoup

url_list = ['http://www.naamkunde.net/?page_id=293&vt_list_male=true', 'http://www.naamkunde.net/?page_id=293&vt_list_female=true']
data = []

for url in url_list:
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    names = html.select("tr > td:nth-of-type(1)")
    for name in names:
        name = name.get_text()
        name = name.replace(" ", "")
        if "(V)" in name: 
            name = name.replace("(V)", "")
            gender = "female"
        if "(M)" in name: 
            name = name.replace("(M)", "")
            gender = "male"
        name = {"name": name, "gender": gender}
        data.append(name)
        print(name)

filename = 'data/dutch_names.json'
with open (filename, 'w') as outfile:
    json.dump(data, outfile)