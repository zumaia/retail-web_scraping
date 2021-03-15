#!/usr/bin/env python
# coding: utf-8

# In[1]:
from bs4 import BeautifulSoup
import pandas as pd
import requests
from functools import reduce
import os

cwd = os.getcwd()
print(cwd)
# In[2]:


with open("data/tienda0.txt", encoding="utf-8") as file:
    tienda0 = [l.rstrip("\n") for l in file]


# In[3]:


tienda0 = tienda0[0]


# In[4]:


# url = input("Enter a website to extract the URL's from: ")

# r  = requests.get("https://" +url)
r = requests.get(tienda0)

data = r.text

soup = BeautifulSoup(data, features="html5lib")

url_data = []

for link in soup.find_all("a"):
    text = link.get("href")
    url_data.append(text)


# In[5]:


# initializing start Prefix
start_letter = tienda0
data_total_url = [x for x in url_data if x.startswith(start_letter)]


# In[6]:


# using naive method to remove duplicated from list
res_data_total_url = []
for i in data_total_url:
    if i not in res_data_total_url:
        res_data_total_url.append(i)


# In[7]:


# Listamos los 10 primeros
res_data_total_url[1:10]


# In[8]:


total_url = []
for i in res_data_total_url:

    r = requests.get(i)

    data = r.text

    soup = BeautifulSoup(data, features="html5lib")

    urls = []

    resulta = soup.find_all("a", attrs={"class": "tc-product-miniature-img"})

    for link in resulta:
        text = link.get("href")
        urls.append(text)

    total_url.append(urls)


# In[9]:


# agrupar listas nested en una


single_list = reduce(lambda x, y: x + y, total_url)


# In[10]:


# Selecciono los que comienzan por
start_letter = tienda0
data_total_url = [x for x in single_list if x.startswith(start_letter)]


# In[11]:


# listo los 10 primeros
data_total_url[1:10]


# In[12]:


# using naive method to remove duplicated from list
res_res_data_total_url = []
for i in data_total_url:
    if i not in res_res_data_total_url:
        res_res_data_total_url.append(i)


# In[13]:


res_res_data_total_url[1:10]


# In[14]:


headers = {
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

r = requests.get(
    "https://twinandchic.com/es/nina/202-4113-vestido-velero.html#/26-talla-2",
    headers=headers,
)

soup = BeautifulSoup(r.content, "html5lib")

total = []

resulta = soup.findAll("section", attrs={"class": "tc-product-content tc-box"})

for link in resulta:
    # desc = link.find('div', attrs = {'class':'url'}).get_text()
    name = link.find("h1", attrs={"class": "tc-product-title tc-title"})
    if name is not None:
        name = name.get_text().strip()
    tipo = link.find("div", attrs={"class": "tc-product-excerpt"})
    if tipo is not None:
        tipo = tipo.get_text().strip()
    price = link.find("span", attrs={"itemprop": "price"})
    if price is not None:
        price = price.get_text().strip()
    description = link.find(
        "div", attrs={"class": "tc-product-info-block isDescription"}
    )
    if description is not None:
        description = description.get_text().strip()
    ref = link.find("span", attrs={"itemprop": "sku"})
    if ref is not None:
        ref = ref.get_text().strip()

    one = {}
    one["name"] = name
    one["tipo"] = tipo
    one["price"] = price
    one["description"] = description
    one["ref"] = ref

    total.append(one)
total


# In[15]:


total_url = []

headers = {
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

for i in res_res_data_total_url:

    r = requests.get(i, headers=headers)

    soup = BeautifulSoup(r.content, "html5lib")

    total = []

    resulta = soup.findAll("section", attrs={"class": "tc-product-content tc-box"})

    for link in resulta:
        # desc = link.find('div', attrs = {'class':'url'}).get_text()
        name = link.find("h1", attrs={"class": "tc-product-title tc-title"})
        if name is not None:
            name = name.get_text().strip()
        tipo = link.find("div", attrs={"class": "tc-product-excerpt"})
        if tipo is not None:
            tipo = tipo.get_text().strip()
        price = link.find("span", attrs={"itemprop": "price"})
        if price is not None:
            price = price.get_text().strip()
        description = link.find(
            "div", attrs={"class": "tc-product-info-block isDescription"}
        )
        if description is not None:
            description = description.get_text().strip()
        ref = link.find("span", attrs={"itemprop": "sku"})
        if ref is not None:
            ref = ref.get_text().strip()

        one = {}
        one["url"] = i
        one["name"] = name
        one["tipo"] = tipo
        one["price"] = price
        one["description"] = description
        one["ref"] = ref

        total.append(one)

    total_url.append(total)


# In[16]:


total_url[1:10]


# In[17]:


single_list = reduce(lambda x, y: x + y, total_url)

df = pd.DataFrame.from_records(single_list)

df


# In[18]:


df["url"] = df["url"].str.replace(tienda0, "tienda0", regex=True)


# In[19]:


df.to_csv("data/tienda_0.csv")
