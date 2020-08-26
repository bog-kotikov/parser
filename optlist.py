from bs4 import BeautifulSoup
import requests
import csv
import time
import re


def sortik(list):
    sortl_all = []

    for row in list:
        try:
            title = str(row['title'].replace(',', ' '))
        except:
            title = row['title']
        try:
            phone = row['phone'].replace(" ", "")
        except:
            phone = 0
        url_c = "https://optlist.ru" + row['url']

        sortl_all.append([title, phone,url_c])



    myFile = open('test.csv', 'a',  encoding='utf-8')
    with myFile:
        writer = csv.writer(myFile, lineterminator='\n' )
        writer.writerows(sortl_all)

    print('Модель                     |         Телефон')
    for row in sortl_all:
        print('{: <80} | {: >24} | {: >13} '.format(row[0], row[1], row[2]))






def parse_avito(par_i,url_i):

    URL = url_i
    HEADERS = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    response = requests.get(URL, headers = HEADERS, params={'page':par_i})
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('h2', class_ ='card-title')
    comps = []

    for item in items:
        comps.append({
            'title': str(item.find('a').get('title')),
            'url'  :  str(item.find('a').get('href'))
              })
    return comps

ip_port = "5.252.192.100:5836"

PROXIES = {
    "https" : "https://" + ip_port,
    "http" : "https://" + ip_port
    }


def parse_phone(url_i):
    URL = 'https://optlist.ru'+ str(url_i) +"/phone_json"
    HEADERS = {
         'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }

    responsejson = requests.get(URL, headers=HEADERS)
    json_response = responsejson.json()
    item = json_response["Phones"]
    phone1 = item[0]
    phone1 = re.sub(r"[+()-]", "", phone1)
    print (phone1)
    return phone1






list_all = []
print(
    "Здрасьте, это парсер оптлист, для работы нужно указать сколько страниц парсить и, собственно, ссылку на нужную категорию")

print("Ссылка оптлист:")
url_av = 'https://optlist.ru/wholesales'

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
    phone = parse_phone(ad["url"])
    ad['phone'] = phone



print ("Всего строк:",len(list_all))

sortik(list_all)