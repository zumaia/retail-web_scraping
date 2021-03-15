#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup
import pandas as pd
import requests
from functools import reduce

# In[2]:


with open("data/tienda2.txt", encoding="utf-8") as file:
    tienda2 = [l.rstrip("\n") for l in file]


# In[3]:


tienda2 = tienda2[0]


# url = input("Enter a website to extract the URL's from: ")
headers = {
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}
# r  = requests.get("https://" +url)

r = requests.get(tienda2, headers)

data = r.text

soup = BeautifulSoup(data, features="html5lib")

url_data = []

for link in soup.find_all("a"):
    text = link.get("href")
    text = str(text).replace("/shop", "shop")
    text = str(text).replace("/shop", tienda2 + "shop")
    text = str(text).replace("shop/", tienda2 + "shop/")
    url_data.append(text)


# initializing start Prefix
start_letter = tienda2 + "shop/"
data_total_url = [x for x in url_data if x.startswith(start_letter)]


# using naive method to remove duplicated from list
res_data_total_url = []
for i in data_total_url:
    if i not in res_data_total_url:
        res_data_total_url.append(i)


total_url = []
for i in res_data_total_url:

    r = requests.get(i)

    data = r.text

    soup = BeautifulSoup(data, features="html5lib")

    urls = []

    resulta = soup.find_all("a", attrs={"class": "anchorGTM"})

    for link in resulta:
        text = link.get("href")
        text = str(text).replace("shop/", tienda2 + "shop/")
        urls.append(text)

    total_url.append(urls)


# In[9]:


# agrupar listas nested en una


single_list = reduce(lambda x, y: x + y, total_url)


# In[10]:


# Selecciono los que comienzan por
start_letter = tienda2 + "shop/articulo/"
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

    resulta = soup.findAll("div", attrs={"class": "cn_product_visited"})

    for link in resulta:
        # desc = link.find('div', attrs = {'class':'url'}).get_text()
        url = link.find("span", attrs={"class": "url"})
        if url is not None:
            url = url.get_text().strip()
        product_id = link.find("span", attrs={"class": "product_id"})
        if product_id is not None:
            product_id = product_id.get_text().strip()
        name = link.find("span", attrs={"class": "name"})
        if name is not None:
            name = name.get_text().strip()
        description = link.find("span", attrs={"class": "description"})
        if description is not None:
            description = description.get_text().strip()
        image_url = link.find("span", attrs={"class": "image_url"})
        if image_url is not None:
            image_url = image_url.get_text().strip()
        unit_price = link.find("span", attrs={"class": "unit_price"})
        if unit_price is not None:
            unit_price = unit_price.get_text().strip()
        category = link.find("span", attrs={"class": "category"})
        if category is not None:
            category = category.get_text().strip()
        type_product = link.find("span", attrs={"class": "type_product"})
        if type_product is not None:
            type_product = type_product.get_text().strip()
        color = link.find("span", attrs={"class": "color"})
        if color is not None:
            color = color.get_text().strip()
        talla = link.find("span", attrs={"class": "talla"})
        if talla is not None:
            talla = talla.get_text().strip()
        one = {}
        one["url"] = url
        one["product_id"] = product_id
        one["name"] = name
        one["description"] = description
        one["image_url"] = image_url
        one["unit_price"] = unit_price
        one["category"] = category
        one["type_product"] = type_product
        one["color"] = color
        one["talla"] = talla

        total.append(one)

    total_url.append(total)


single_list = reduce(lambda x, y: x + y, total_url)

df = pd.DataFrame.from_records(single_list)

df["url"] = df["url"].str.replace(tienda2, "tienda2", regex=True)
df["image_url"] = df["image_url"].str.replace(tienda2, "tienda2", regex=True)

df.to_csv("data/tienda_2.csv")
