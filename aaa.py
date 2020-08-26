from bs4 import BeautifulSoup
import requests
import csv



def parse_avito(par_i,url_i):

    URL = url_i
    HEADERS = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    response = requests.get(URL, headers = HEADERS, params={'p':par_i})
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ ='description item_table-description')
    comps = []

    # 'title': str(item.find('a', class_='snippet-link').get_text(strip=True))[:-6],
    # 'year': str(item.find('a', class_='snippet-link').get_text(strip=True))[-4:],

    for item in items:
        comps.append({
            'title': str(item.find('a', class_= 'snippet-link').get_text(strip=True)),
            'year' : str(item.find('a', class_= 'snippet-link').get_text(strip=True)),
            'price': str(item.find('span', class_='snippet-price').get_text(strip=True)).strip("  ₽"),
            'url'  : 'avito.ru' + item.find('a', class_= 'snippet-link').get('href'),
            'page_nmb': par_i
              })
    return comps

def parse_auto(par_i, url_i):

    URL = url_i
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS, params={'page': par_i})
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='ListingItem-module__main')

    comps = []

    for item in items:
        try:
            comps.append({
            'title': item.find('a', class_='Link ListingItemTitle-module__link').get_text(strip=True),
            'year': item.find('div', class_='ListingItem-module__year').get_text(strip=True),
            'price': str(item.find('div', class_='ListingItemPrice-module__content').get_text(strip=True)).strip("  ₽"),
            'url': item.find('a', class_='Link ListingItemTitle-module__link').get('href'),
            'page_nmb': par_i
            })
        except:
            comps.append({
                'title': item.find('a', class_='Link ListingItemTitle-module__link').get_text(strip=True),
                'year': item.find('div', class_='ListingItem-module__year').get_text(strip=True),
                'price': " 0",
                'url': item.find('a', class_='Link ListingItemTitle-module__link').get('href'),
                'page_nmb': par_i
            })


    return comps


# for comp in comps:
# print (comp['title']+ " - " + comp['price'])
# print (f"Средняя стоимость - {average(comps)} руб.")

def sortik(list):
    sortl_all = []


    for row in list:
        row['price'] = row['price'].replace('от', '')
        row['price'] = row['price'].replace(' ', '')
        title = row['title']
        year = row['year']
        price = row['price'].replace(',', '')
        url_c = row['url']
        page_nmb = 0 + 1
        sortl_all.append([title,year, price,  url_c, page_nmb])

    #sortl_all.sort(key=lambda row: row[1])  #сортировка по году

    myFile = open('test.csv', 'w')
    with myFile:
        writer = csv.writer(myFile, lineterminator='\n')
        writer.writerows(sortl_all)

    print('Модель                     |         Цена')
    for row in sortl_all:
        print('{: <40} | {: >24} | {: >13} | {:}'.format(
            row[0], row[1], row[2], row[3],row[4]))


list_all = []
print(
    "Здрасьте, это авито\автору парсер, для работы нужно указать сколько страниц парсить и, собственно, ссылку на нужную категорию")

print("Ссылка авито:")
url_av = input()

print("Введите кол-во страниц")
list_countav = input()

print("Ссылка авто ру:")
url_ia = input()

print("Введите кол-во страниц")
list_counta = input()



for i in range(1,int(list_countav)):
    complete = (int(i) / int(list_countav)) * 100
    print('Авито готово:', int(complete),"%")
    new_list = parse_avito(i, url_av)
    list_all.extend(new_list)

print ("У авито строк:",len(list_all))

for i in range(1,int(list_counta)):
    complete = (int(i) / int(list_counta)) * 100
    print('Авто ру готово:', int(complete),"%")
    new_list = parse_auto(i, url_ia)
    list_all.extend(new_list)

print ("Всего строк:",len(list_all))

sortik(list_all)