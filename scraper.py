import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

data = {"name":[], "label":[], "price":[]}
term = input("->")

amazon_data = BeautifulSoup(requests.get(url='https://www.amazon.in/s', params={'k':term}).text, features="html.parser")
for i in amazon_data.findAll('div', attrs={'class': 's-include-content-margin'}):
    item = i.find('span', attrs={'class':'a-text-normal'})
    price = i.find('span', attrs={'class':'a-price-whole'})
    if price is not None:
        data["label"].append("amazon")
        data["name"].append(item.get_text())
        data["price"].append(int(re.sub("\D", "", price.get_text())))
        break
    

term = data[0]["name"] if len(data)==1 else term

flipkart_data = BeautifulSoup(requests.get(url='https://www.flipkart.com/search', params={'q': term}).text, features="html.parser")
for a in flipkart_data.findAll('a',href=True, attrs={'class':'_31qSD5'}):
    name=a.find('div', attrs={'class':'_3wU53n'})
    price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
    if name is not None and price is not None:
        data["label"].append("flipkart")
        data["name"].append(item.get_text())
        data["price"].append(int(re.sub("\D", "", price.get_text())))
        break

paytm_data = BeautifulSoup(requests.get(url='https://paytm.com/shop/search', params={'q':term}).text, features="html.parser")
for a in paytm_data.findAll('div', attrs={'class':'_2i1r'}):
    name=a.find('div', attrs={'class':'_2apC'})
    price=a.find('span', attrs={'class':'_1kMS'})
    if name is not None and price is not None:
        data["label"].append("paytm")
        data["name"].append(item.get_text())
        data["price"].append(int(re.sub("\D", "", price.get_text())))
        break

df = pd.DataFrame(data)
print(df)
x = df.iloc[:,1], y = df.iloc[:,2]
x_pos = np.arange(len(x))
plt.bar(x_pos, y, color='#7ed6df')
plt.xlabel("Websites")
plt.ylabel("Price")
plt.title("Online Price Comparison")
plt.xticks(x_pos, x)
plt.show()

