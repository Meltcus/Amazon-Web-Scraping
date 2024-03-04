# This program creates a webscraper to scrape data from an amazon page of items. It organizes each link of an item in a dictionary
# and then sorts through each variable (Title, Price, Rating) into its own list which as a whole gets appended to a dictionnary Item

# Progress: Final Touches (Add Reviews and Stock)

import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys

URL = "https://www.amazon.in/s?k=samsung+odyssey+g7&crid=266R0T07B33VE&sprefix=Samsun+Ody%2Caps%2C111&ref=nb_sb_ss_ts-doa-p_1_10"

# Headers for request
HEADERS = ({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

# HTTP Request
webpage = requests.get(URL, headers=HEADERS)

# webpage has to have "<Response [200]>" in order to proceed
# Soup Object containing all data
soup = BeautifulSoup(webpage.content, "html.parser")

# Fetch links tag as List of Tag Objects - Stored in an array of lists
links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})  # Class description of a link in html

links_list = []

# Stores each link into the array/list
for link in links:
    links_list.append(link.get('href'))

Item = {"title":[], "price":[], "rating":[] }

for link in links_list:
    new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

    # Soup Object containing all data
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    # Getting the Title
    Item['title'].append(new_soup.find("span", attrs={"id": 'productTitle'}).text.strip())

    # Getting the Price
    Item['price'].append(new_soup.find("span", attrs={"class": 'a-price-whole'}).text.replace(".",""))

    # Getting the Rating
    Item['rating'].append(new_soup.find("span", attrs={"class": 'a-icon-alt'}).text)


amazon_df = pd.DataFrame.from_dict(Item)
amazon_df['title'].replace('', np.nan, inplace=True)
amazon_df = amazon_df.dropna(subset=['title'])
amazon_df.to_csv("amazon_data.csv", header=True, index=False)

print(amazon_df)