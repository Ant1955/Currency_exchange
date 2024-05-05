import requests
import re
from bs4 import BeautifulSoup
val_matrix = [["" for _ in range(5)] for _ in range(50)]
# 
session = requests.Session()
# URL поиска
search_url = 'https://www.cbr.ru/currency_base/daily/'
# 'https://www.google.com/search?q=Курс+доллара+ЦБ&sourceid=chrome&ie=UTF-8'
response = session.get(search_url)
# Парсинг ответа для извлечения необходимых данных
soup = BeautifulSoup(response.text, 'html.parser')
# Предположим, что результаты поиска находятся в каком-то блоке с классом 'search-results'
results = soup.find_all(re.compile(r'div', re.I),class_="table")
tr_elements = results[0].find_all('tr')
i = 0
k = 0
for tds in tr_elements[1:]:
  for td in tds:
    if td.get_text().strip() != '':
      val_matrix[i][k] = td.get_text().strip()
      k += 1
      if k == 5:
        i += 1
        k = 0
print ("курс ЦБ на сегодня\nкод	Букв.код Единиц Курс рубля  наименование")
imax = i
for i in range(imax):
  print (val_matrix[i][0], val_matrix[i][1],"\t", val_matrix[i][2],"\t",val_matrix[i][4],"\t\t", val_matrix[i][3])

while True:
    try:
      action = input("Вы хотите купить или продать валюту? ").lower()
      act = None
      if "куп" in action :
        act = "купить" 
      elif "прод" in action:
        act = "продать"
      if act == None:
        print ("Введите купить или продать")
        continue
      break
    except ValueError:
      print("Пожалуйста, выберите действие")
while True:
    try:
      currency = input("введите код валюты или название: ")
      exch = None
      count_row = 0
      for i in range(imax):
        if currency in val_matrix[i][3].lower() or currency.upper() == val_matrix[i][1] or currency == val_matrix[i][0]:
          exch = float(val_matrix[i][4].replace(',', '.'))
          currency_name = val_matrix[i][3]
          count_row += 1
      if exch == None:
        print(f"Извините, этой валюты нет\nВведите другой код валюты\n {currency}")
        continue
      if count_row != 1:
        confirm = input(f"Вы ввели '{currency}' это соответствует нескольким вариантам\nВы точно хотите {act} {currency_name} ([y]/n) ?")
        if confirm != 'y' and confirm != '' and confirm != 'да':
          continue
      break
    except ValueError:
      print("Пожалуйста, уточните код валюты ")
while True:
    try:
      amount = float( input(f"введите количество {currency_name} ") )
      if amount <= 0 or amount % 1 != 0 :
        print (f"Вы можете {act} только целое положительное число {currency_name}")
        continue
      break
    except ValueError:
      print(f"Пожалуйста, уточните количество {currency_name}")
rubl = int(amount * exch // 1)
kop = int(( amount * exch % 1 ) * 100 )
if act == "купить" :
  print(f"внесите {rubl} рублей {kop} копеек")
elif act == "продать" :
  print(f"получите {rubl} рублей {kop} копеек")
else:
  print("Извините, но мы не можем выполнить эту операцию")