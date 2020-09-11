import requests
from bs4 import BeautifulSoup
import re
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

data = []
search_term = input("Enter product name:")

amazon_data = BeautifulSoup(requests.get(url='https://www.amazon.in/s', params={'k':search_term}).text, features="html.parser")
items = amazon_data.findAll('div', attrs={'class': 's-include-content-margin'})

for item in items:
    name = item.find('span', attrs={'class':'a-text-normal'})
    price = item.find('span', attrs={'class':'a-price-whole'})
    if price is not None:
        temp = {}
        temp["label"] = "amazon"
        temp["name"] = name.get_text()
        temp["price"] = int(re.sub(r"\D", "", price.get_text()))
        data.append(temp)
        break
    

search_term = data[0]["name"] if len(data)==1 else search_term

flipkart_data = BeautifulSoup(requests.get(url='https://www.flipkart.com/search', params={'q': search_term}).text, features="html.parser")
items = flipkart_data.findAll('a',href=True, attrs={'class':'_31qSD5'})

for item in items:
    name=item.find('div', attrs={'class':'_3wU53n'})
    price=item.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
    if name is not None and price is not None:
        temp = {}
        temp["label"] = "flipkart"
        temp["name"] = name.get_text()
        temp["price"] = int(re.sub(r"\D", "", price.get_text()))
        data.append(temp)
        break

paytm_data = BeautifulSoup(requests.get(url='https://paytm.com/shop/search', params={'q':search_term}).text, features="html.parser")
items = paytm_data.findAll('div', attrs={'class':'_2i1r'})

for item in items:
    name=item.find('div', attrs={'class':'_2apC'})
    price=item.find('span', attrs={'class':'_1kMS'})
    if name is not None and price is not None:
        temp = {}
        temp["label"] = "paytm"
        temp["name"] = name.get_text()
        temp["price"] = int(re.sub(r"\D", "", price.get_text()))
        data.append(temp)
        break

for item in data:
    print(item["label"], item["name"], item["price"])

x = list(map(lambda item: str(item['label']) + ' - ' + str(item['name']), data))
y = list(map(lambda item: item['price'], data))
plt.bar(x,y, bottom=0)
plt.xlabel("Websites")
plt.ylabel("Price")
plt.title("Online Price Comparison")
plt.show()
