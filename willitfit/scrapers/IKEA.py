'''
Receives list of article codes and article counts.
Scrapes IKEA website to obtain package dimensions (rounded up to next cm), weights (in kg rounded up 2 decimals) and counts.
Returns list of package dimensions and weights.
'''

from willitfit.params import IKEA_COUNTRY_DOMAIN, IKEA_WEBSITE_LANGUAGE
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import requests
import pandas as pd
import chromedriver_binary


IKEA_URL = f"https://www.ikea.com/{IKEA_COUNTRY_DOMAIN}/{IKEA_WEBSITE_LANGUAGE}"
IKEA_SEARCH_URL = f"/search/products/?q="


def chrome_settings():
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--window-size=1920x1080') 
    
    return chrome_options

def scrap_product(article_code, item_count):
    
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_settings())
    driver.get(IKEA_URL+IKEA_SEARCH_URL+f'{article_code}')
    important_part_of_page = driver.find_element_by_class_name('results__list')
    tag = important_part_of_page.find_element_by_tag_name('a')
    #https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen
    driver.execute_script("arguments[0].click();", tag)
    soup = BeautifulSoup(driver.page_source, 'html.parser')  
    important_part_of_page = soup.find_all("div",  {"id": 'SEC_product-details-packaging'})
    
    return important_part_of_page[0]

def extract_numeric_product_to_dict(product_features):
    
    info_dict = {}
    new_columns_name = ['width','high','length','weight','packeges']
    for info in product_features:
        info_item = info.split()
        for i,x in enumerate(info_item):            
            try:
                float(x)
                info_dict[info_item[0]] = float(info_item[1])          
            except:
                pass
    info_dict = {x:y for x,y in zip(new_columns_name,info_dict.values())}
    
    return info_dict

def packages_dimensions_weights(page):
    info = page.find_all('div',  {"class": 'range-revamp-product-details__container'})
    number = page.find_all('span',  {"class": 'range-revamp-product-identifier__value'})

    list_of_products = []
    product_info = {}
    for i,(x,y) in enumerate(zip(number,info)):
        y_info = [info.text for info in y.find_all('span',  {"class": 'range-revamp-product-details__label'})]
        product_info = extract_numeric_product_to_dict(y_info) 
        product_info['subarticle_code'] = x.text.replace('.','')        
        
        list_of_products.append(product_info)
        
    return pd.DataFrame(list_of_products)

def product_info_and_update_csv_database(article_code,path_to_csv):
    
    ikea_database = pd.read_csv(path_to_csv,index_col = [0])
    all_ordered_product_df = pd.DataFrame()
    new_product_for_database = pd.DataFrame()
    
    for i,x in enumerate(article_code):
        if ikea_database.shape[0]>0 and (ikea_database['article_code'] == x).any():
            all_ordered_product_df = all_ordered_product_df.append(ikea_database[ikea_database['article_code'] == x])
        else:
            page = scrap_product(x,item_count=None)
            df = packages_dimensions_weights(page)
            df['article_code'] = article_code[i]
            all_ordered_product_df = all_ordered_product_df.append(df)
            new_product_for_database = new_product_for_database.append(df)
            
    ikea_database = ikea_database.append(new_product_for_database)
    ikea_database.to_csv(path_to_csv)
    return all_ordered_product_df