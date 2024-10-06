# %%
from pyheaven import *
import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd

def CrawlPonies(url, fixed_category=None, table_class="wikitable sortable listofponies"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_=table_class)

    # Extract the table data and store it in a list of lists
    data = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):
            row_data.append(cell)
        if len(row_data)>2:
            data.append(row_data)

    names = [row[0] for row in data]
    categories = [row[1] for row in data]
    images = [row[-1] for row in data]
    
    # Keep only the bolded text in the name
    names = [cell.find('b').text.strip() if cell.find('b') else cell.text.strip() for cell in names]
    
    # Keep only the text in the category
    categories = [cell.text.strip() for cell in categories]
    
    # Get the image urls in the last column's data-src attribute
    images = [cell.find('a')['href'] if cell.find('a') else None for cell in images]
    
    # Download the images and save them with the corresponding name
    for name, image, category in TQDM(list(zip(names, images, categories)), desc=url):
        try:
            c = fixed_category if fixed_category else category
            CreateFolder(pjoin("extracted", c))
            n = name.replace('/','_')
            if image and not ExistFile(pjoin("extracted", c, f"{n}.png")):
                with open(pjoin("extracted", c, f"{n}.png"), 'wb') as f:
                    f.write(requests.get(image).content)
        except Exception as e:
            print(e)

# %%
# CrawlPonies(url="https://mlp.fandom.com/wiki/List_of_non-pony_characters")

CrawlPonies(url="https://mlp.fandom.com/wiki/List_of_ponies/Earth_ponies", fixed_category="Earth")
CrawlPonies(url="https://mlp.fandom.com/wiki/List_of_ponies/Pegasus_ponies", fixed_category="Pegasus")
CrawlPonies(url="https://mlp.fandom.com/wiki/List_of_ponies/Unicorn_ponies", fixed_category="Unicorn")
CrawlPonies(url="https://mlp.fandom.com/wiki/List_of_ponies/Alicorn_ponies", fixed_category="Alicorn")
# %%
