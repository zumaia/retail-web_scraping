#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
from functools import reduce

# In[2]:


with open("data/tienda1.txt", encoding="utf-8") as file:
    tienda1 = [l.rstrip("\n") for l in file]


# In[3]:


tienda1


# In[4]:


# url = input("Enter a website to extract the URL's from: ")
headers = {
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}
# r  = requests.get("https://" +url)
r = requests.get(tienda1[0], headers)

data = r.text

soup = BeautifulSoup(data, features="html5lib")

url_data = []

for link in soup.find_all("a"):
    text = link.get("href")
    text = str(text).replace("'", "")
    url_data.append(text)


# In[5]:


# initializing start Prefix
start_letter = "https://"
data = [x for x in url_data if x.startswith(start_letter)]


# In[6]:


# data


# In[7]:


# initializing start Prefix
start_letter = tienda1[0]
data_list = [x for x in data if x.startswith(start_letter)]
end_letter = ".html"
data_list1 = [x for x in data_list if x.endswith(end_letter)]

# data_list1


# In[8]:


total_url = []
for i in data_list1:

    r = requests.get(i)

    data = r.text

    soup = BeautifulSoup(data, features="html5lib")

    urls = []

    for link in soup.find_all("a"):
        text = link.get("href")
        text = str(text).replace("'", "")
        urls.append(text)

    total_url.append(urls)


# In[9]:


# total_url


# In[10]:


# agrupar listas nested en una


single_list = reduce(lambda x, y: x + y, total_url)


# In[11]:


# initializing start Prefix
start_letter = tienda1[0]
data_total_url = [x for x in single_list if x.startswith(start_letter)]



# In[12]:





# In[13]:


len(data_total_url)


# In[14]:


# using naive method to remove duplicated from list
res_data_total_url = []
for i in data_total_url:
    if i not in res_data_total_url:
        res_data_total_url.append(i)


# In[15]:


len(res_data_total_url)




# In[18]:


total_url = []

headers = {
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

for i in res_data_total_url:

    r = requests.get(i, headers=headers)

    soup = BeautifulSoup(r.content, "html5lib")

    total = []

    resulta = soup.findAll("div", attrs={"class": "product-info-main"})

    for link in resulta:
        # desc = link.find('div', attrs = {'class':'url'}).get_text()
        base = link.find("span", attrs={"class": "base"})
        if base is not None:
            base = base.get_text()
        title = link.find("span", attrs={"class": "section-title"})
        if title is not None:
            title = title.get_text()
        description = link.find("span", attrs={"itemprop": "description"})
        if description is not None:
            description = description.get_text()
        sku = link.find("span", attrs={"itemprop": "sku"})
        if sku is not None:
            sku = sku.get_text()
        color_value = link.find("span", attrs={"id": "color-swatch-value"})
        if color_value is not None:
            color_value = color_value.get_text()
        price = link.find("span", attrs={"class": "price"})
        if price is not None:
            price = price.get_text()
        color = link.find("img", attrs={"class": "color-value"})
        if color is not None:
            color = color.get_text()
        one = {}
        one["url"] = i
        one["base"] = base
        one["title"] = title
        one["description"] = description
        one["sku"] = sku
        one["color_valuecolor_value"] = color_value
        one["price"] = price
        one["color"] = color

        total.append(one)

    total_url.append(total)


# In[19]:


single_list = reduce(lambda x, y: x + y, total_url)

df = pd.DataFrame.from_records(single_list)

df["url"] = df["url"].str.replace(tienda1[0], "tienda1", regex=True)


# In[20]:


df.to_csv("data/tienda_1.csv")
