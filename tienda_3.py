#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
from functools import reduce


with open("data/tienda3.txt", encoding="utf-8") as file:
    tienda3 = [l.rstrip("\n") for l in file]


tienda3 = tienda3[0]
tienda3


# url = input("Enter a website to extract the URL's from: ")
headers = {
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}
# r  = requests.get("https://" +url)
r = requests.get(tienda3, headers)

data = r.text

soup = BeautifulSoup(data, "html5lib")

url_data = []

for link in soup.find_all("a"):
    text = link.get("href")
    url_data.append(text)


# to remove None values in list
res = []
for val in url_data:
    if val != None:
        res.append(val)


start_letter = tienda3
data_total_url = [k for k in res if start_letter in k]


# using naive method to remove duplicated from list
res_data_total_url = []
for i in data_total_url:
    if i not in res_data_total_url:
        res_data_total_url.append(i)


total_url = []
for i in res_data_total_url:

    r = requests.get(i)

    data = r.text

    soup = BeautifulSoup(data, "html5lib")

    urls = []

    resulta = soup.find_all(
        "a", attrs={"class": "product photo product-item-photo ez-gallery-anchor"}
    )

    for link in resulta:
        text = link.get("href")
        urls.append(text)

    total_url.append(urls)


# agrupar listas nested en una

single_list = reduce(lambda x, y: x + y, total_url)


# Selecciono los que comienzan por
start_letter = tienda3
data_total_url = [x for x in single_list if x.startswith(start_letter)]


# using naive method to remove duplicated from list
res_res_data_total_url = []
for i in data_total_url:
    if i not in res_res_data_total_url:
        res_res_data_total_url.append(i)


# webscarping total

total_url = []

headers = {
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

for i in res_res_data_total_url:

    r = requests.get(i, headers=headers)

    soup = BeautifulSoup(r.content, "html5lib")

    total = []

    resulta = soup.findAll("div", attrs={"class": "product-info-sidebar"})

    for link in resulta:
        # desc = link.find('div', attrs = {'class':'url'}).get_text()
        base = link.find("span", attrs={"class": "base"})
        if base is not None:
            base = base.get_text()
        price = link.find("span", attrs={"class": "price"})
        if price is not None:
            price = price.get_text()
        value = link.find("div", attrs={"class": "value"})
        if value is not None:
            value = value.get_text()
        description = link.find("div", attrs={"itemprop": "description"})
        if description is not None:
            description = description.get_text()
        image_url = link.find("span", attrs={"class": "image_url"})
        if image_url is not None:
            image_url = image_url.get_text()
        unit_price = link.find("span", attrs={"class": "unit_price"})
        if unit_price is not None:
            unit_price = unit_price.get_text()
        category = link.find("span", attrs={"class": "category"})
        if category is not None:
            category = category.get_text()
        type_product = link.find("span", attrs={"class": "type_product"})
        if type_product is not None:
            type_product = type_product.get_text()
        color = link.find("span", attrs={"class": "color"})
        if color is not None:
            color = color.get_text()
        talla = link.find("span", attrs={"class": "talla"})
        if talla is not None:
            talla = talla.get_text()
        one = {}
        one["url"] = i
        one["base"] = base
        one["price"] = price
        one["value"] = value
        one["description"] = description

        total.append(one)

    total_url.append(total)


single_list = reduce(lambda x, y: x + y, total_url)

df = pd.DataFrame.from_records(single_list)

df["url"] = df["url"].str.replace(tienda3, "tienda3", regex=True)


df.to_csv("data/tienda_3.csv")
