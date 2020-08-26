from bs4 import BeautifulSoup
import requests
import csv
import time



def parse_avito(par_i,url_i):

    URL = url_i
    HEADERS = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    response = requests.get(URL, headers = HEADERS, params={'p':par_i})
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ ='description item_table-description')
    comps = []

    for item in items:
        try:
            ad_numb = str(item.find('a', class_='snippet-link').get('href')).rsplit("_", maxsplit=1)[1]
        except:
            ad_numb = 0
        comps.append({
            'title': str(item.find('a', class_= 'snippet-link').get_text(strip=True)),
            'price': str(item.find('span', class_='snippet-price').get_text(strip=True)).strip("  ₽"),
            'url'  : 'm.avito.ru' + item.find('a', class_= 'snippet-link').get('href'),
            'ad_nmb': ad_numb
              })
    return comps

def parse_phone(url_i):
    URL = 'https://m.avito.ru/api/1/items/'+ str(url_i) + '/phone'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS, params={'key':"af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"})
    json_response = response.json()
    try:
        result = json_response['result']
        action = result['action']
        phone = str(action['uri'])[-11:]
        return phone
    except:
        return 0





# for comp in comps:
# print (comp['title']+ " - " + comp['price'])
# print (f"Средняя стоимость - {average(comps)} руб.")

def sortik(list):
    sortl_all = []

    for row in list:
        row['price'] = row['price'].replace('от', '')
        row['price'] = row['price'].replace(' ', '')
        try:
            price = int(row['price'].replace(' ', ''))
        except:
            price = "не указана"
        try:
            title = str(row['title'].replace(',', ' '))
        except:
            title = row['title']
        try:
            phone = row['phone']
        except:
            phone = 0
        url_c = row['url']
        #page_nmb = row['ad_nmb']


        sortl_all.append([title,price, phone,url_c])

    #sortl_all.sort(key=lambda row: row[1])  #сортировка по году

    myFile = open('test.csv', 'w',  encoding='utf-8')
    with myFile:
        writer = csv.writer(myFile, lineterminator='\n' )
        writer.writerows(sortl_all)

    print('Модель                     |         Цена')
    for row in sortl_all:
        print('{: <40} | {: >24} | {: >13}  | {:}'.format(
            row[0], row[1], row[2],row[3]))


list_all = []
print(
    "Здрасьте, это авито\автору парсер, для работы нужно указать сколько страниц парсить и, собственно, ссылку на нужную категорию")

print("Ссылка авито:")
url_av = input()

print("Введите кол-во страниц")
list_countav = input()

count = 0


for i in range(1,int(list_countav)):
    complete = (int(i) / int(list_countav)) * 100
    print('Страницы готовы:', int(complete),"%")
    new_list = parse_avito(i, url_av)
    list_all.extend(new_list)

for ad in list_all:
    count = count + 1
    complete = (count / len(list_all)) * 100
    print('Номера готовы:', int(complete), "%")
    try:
        phone = parse_phone(ad["ad_nmb"])
        ad['phone'] = phone
    except:
        print ("Ошибка, засыпаю")
        print (phone)
        time.sleep(10)


print ("Всего строк:",len(list_all))

sortik(list_all)