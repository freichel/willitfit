import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Scrape uri from each page
## Populate uri_list
uri_list = []

BASE_URL = 'http://www.ridc.org.uk/features-reviews/out-and-about/choosing-car/car?page='
MAX_PAGE = 157

## Pagination
for page in range(1, MAX_PAGE+1):
    print(f"Parsing page {page}...")

    PAGE_URL = BASE_URL+f'{page}'
    response = requests.get(PAGE_URL)
    page_soup = BeautifulSoup(response.content, "html.parser")
    
    for item in page_soup.find_all(class_="views-field views-field-title views-align-left"):
        uri_list.append(item.find('a').attrs['href'])


# Scrape through every uri
SCRAPE_BASE_URL = 'http://www.ridc.org.uk'

## Compile regex to parse numerical fields
rx = re.compile(r'(\d*)mm')

## Populate dictionary
df_dict = {
    'make': [],
    'car_model': [],
    'depth': [],
    'height': [],
    'width': []
}
for uri in uri_list:
    PAGE_URL = SCRAPE_BASE_URL+f'{uri}'
    response = requests.get(PAGE_URL)
    page_soup = BeautifulSoup(response.content, "html.parser")
    
    car_model = page_soup.find('h1').text
    make = page_soup.find(class_='field--name-field-make').find('a').text
    depth = int(int(
            rx.findall(
                page_soup.find(
                    class_='field--name-field-length-of-boot-floor-back')
                .text)[0])/10)
    height =int(int(
            rx.findall(
                page_soup.find(class_='field--name-field-vertical-height-of-boot-op')
                .text)[0])/10)
    width = int(int(
            rx.findall(page_soup.find(class_='field--name-field-width-of-boot-floor-at-nar')
                       .text)[0])/10)
    df_dict['make'].append(make)
    df_dict['car_model'].append(car_model)
    df_dict['depth'].append(depth)
    df_dict['height'].append(height)
    df_dict['width'].append(width)
    
data = pd.DataFrame(df_dict)
# Clean data
data['car_model'] = data['car_model'].str.replace('\n', '')
## Optional: Make model names upper case
data['car_model'] = data['car_model'].str.upper()

## Function for removing duplicated 'make' names in 'car_model' and strip trailing whitespace
def remove_make(df):
    make = df['make'].upper()
    if make in df['car_model']:
        df['car_model'] = df['car_model'].replace(make, '').strip()
    return df

data = data.apply(remove_make, axis=1)

## Drop Duplicates 
data.drop(index=data[data['car_model'].duplicated()].index, inplace=True)

## Export as csv
data.to_csv('cars_clean.csv', index=False)