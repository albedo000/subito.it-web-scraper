from bs4 import BeautifulSoup
import requests
from csv import writer

url = "https://www.subito.it/annunci-italia/vendita/auto/"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all('div', class_="item-card")

with open('cars_subito.csv', 'w', encoding='utf8', newline='') as f:
    writ = writer(f)
    header = ['Modello', 'Prezzo', 'Località', 'Provincia',
              'Usato', 'Data', 'Km', 'Alimentazione', 'Cambio', 'Euro']
    writ.writerow(header)

    for item in results:
        title = item.find('h2').text
        price = item.find('p').text
        locality = item.find(
            'span', class_="index-module_sbt-text-atom__ed5J9 index-module_token-caption__TaQWv index-module_size-small__XFVFl index-module_weight-semibold__MWtJJ index-module_town__2H3jy").text
        province = item.find('span', class_="city").text
        specs = item.find_all(
            'p', class_="index-module_sbt-text-atom__ed5J9 index-module_token-body__GXE1P index-module_size-small__XFVFl index-module_weight-book__WdOfA index-module_info__GDGgZ")
        list = []
        if len(specs) < 6:
            difference = 6 - len(specs)
            for i in range(6 - difference):
                specs[i] = specs[i].text
            for i in range(difference):
                specs.append('')
            list = specs
        else:
            for i in range(len(specs)):
                list.append(specs[i].text)
        usato, data, km, carburante, cambio, euro = list
        info = [title, price, locality, province,
                usato, data, km, carburante, cambio, euro]
        writ.writerow(info)
