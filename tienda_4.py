#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
from functools import reduce


# In[2]:


with open("data/tienda4.txt", encoding="utf-8") as file:
    tienda4 = [l.rstrip("\n") for l in file]


# In[3]:


tienda4 = tienda4[0]


# In[4]:


headers = {
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

# r  = requests.get("https://" +url)


r = requests.get(tienda4, headers=headers)

soup = BeautifulSoup(r.content, "html5lib")


url_data = []

for link in soup.find_all("a"):
    text = link.get("href")
    url_data.append(text)


# to remove None values in list
res = []
for val in url_data:
    if val != None:
        res.append(val)


# In[7]:


# Seleccionamos los elementos que comienzan por
start_letter = tienda4
data_total_url = [k for k in res if start_letter in k]


# using naive method to remove duplicated from list
res_data_total_url = []
for i in data_total_url:
    if i not in res_data_total_url:
        res_data_total_url.append(i)


# In[11]:


total_url = []
for i in res_data_total_url:

    headers = {
        "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

    r = requests.get(i, headers=headers)

    data = r.text

    soup = BeautifulSoup(data, "html5lib")

    urls = []

    resulta = soup.find_all("a", attrs={"class": "product-image"})

    for link in resulta:
        text = link.get("href")
        urls.append(text)

    total_url.append(urls)


# agrupar listas nested en una

single_list = reduce(lambda x, y: x + y, total_url)


# Selecciono los que comienzan por
start_letter = tienda4
data_total_url = [x for x in single_list if x.startswith(start_letter)]


# using naive method to remove duplicated from list
res_res_data_total_url = []
for i in data_total_url:
    if i not in res_res_data_total_url:
        res_res_data_total_url.append(i)


total_url = []

headers = {
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

for i in res_res_data_total_url:

    r = requests.get(i, headers=headers)

    soup = BeautifulSoup(r.content, "html5lib")

    total = []

    resulta = soup.findAll(
        "div",
        attrs={"class": "product-shop-wrapper columns xsmall-12 small-12 medium-3"},
    )

    for link in resulta:
        # desc = link.find('div', attrs = {'class':'url'}).get_text()
        name = link.find("div", attrs={"class": "product-name"})
        if name is not None:
            name = name.get_text().strip()
        price = link.find("span", attrs={"class": "price"})
        if price is not None:
            price = price.get_text().strip()
        color = link.find("span", attrs={"class": "product-color-value"})
        if color is not None:
            color = color.get_text().strip()
        description = link.find("div", attrs={"class": "content"})
        if description is not None:
            description = description.get_text().strip()
        composition = link.find("span", attrs={"class": "composition"})
        if composition is not None:
            composition = composition.get_text().strip()
        sku = link.find("p", attrs={"class": "product-sku"})
        if sku is not None:
            sku = sku.get_text().strip()

        one = {}
        one["url"] = i
        one["name"] = name
        one["price"] = price
        one["color"] = color
        one["description"] = description
        one["composition"] = composition
        one["sku"] = sku

        total.append(one)

    total_url.append(total)


single_list = reduce(lambda x, y: x + y, total_url)

df = pd.DataFrame.from_records(single_list)

df["url"] = df["url"].str.replace(tienda4, "tienda4", regex=True)


# In[23]:


df.to_csv("data/tienda_4.csv")
