"""
Receives list of article codes and article counts.
Scrapes IKEA website to obtain package dimensions (rounded up to next cm), weights (in kg rounded up 2 decimals) and counts.
Returns list of package dimensions and weights.
"""

from willitfit.params import (
    DTYPE_DICT,
    IKEA_COUNTRY_DOMAIN,
    IKEA_WEBSITE_LANGUAGE,
    PROJECT_DIR,
    PROJECT_NAME,
    WEBSITE_UNAVAILABLE,
    ARTICLE_NOT_FOUND,
    DATA_FOLDER,
    ARTICLE_DATABASE,
    IKEA_DATABASE_DTYPES,
)
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from willitfit.app_utils.googlecloud import get_cloud_data, send_cloud_data

import os
import requests
import pandas as pd
import chromedriver_binary
# Define path to database
DATABASE_PATH = DATA_FOLDER + "/" + ARTICLE_DATABASE


def chrome_settings():
    """ """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return chrome_options


def prepare_url(
    article_code,
    country_domain=IKEA_COUNTRY_DOMAIN,
    website_language=IKEA_WEBSITE_LANGUAGE):
    """
    Function prapare url for scraper, which is unique for every article
    """

    IKEA_URL = f"https://www.ikea.com/{country_domain}/{website_language}/"
    IKEA_SEARCH_URL = f"search/products/?q="
    url = os.path.join(IKEA_URL, IKEA_SEARCH_URL + article_code)
    return url

def check_if_item_exists(url):
    """
    check if item exists on website.
    If webiste doesn't exists return "Website temporarily unavailable."
    """
    r = requests.get(url)
    if r.status_code == 404:
        return WEBSITE_UNAVAILABLE


def scrape_product(url):
    """
    Scrape the article from Ikea website
    Return page source
    """

    # Setup driver
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_settings()
    )

    # Scrape website and select relevant part of the website
    driver.get(url)
    try:
        html = driver.find_element_by_class_name("results__list")
        # Check if the article exists, if not return str
        html = html.find_element_by_tag_name("a")
    except:
        return ARTICLE_NOT_FOUND
    # if article exists return important part of page
    # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen
    driver.execute_script("arguments[0].click();", html)
    return driver.page_source



def extract_inforamtion_from_html(html):

    page = BeautifulSoup(html, "html.parser")
    page = page.find_all(
        "div", {"id": "SEC_product-details-packaging"}
    )[0]
    # filter out important info with beautiful soup
    info = page.find_all("div", {"class": "range-revamp-product-details__container"})
    number = page.find_all("span", {"class": "range-revamp-product-identifier__value"})
    product_name = page.find_all(
        "span", {"class": "range-revamp-product-details__header notranslate"}
    )[0].text

    return info, number, product_name

def extract_dimensions_from_bs4(dimension_info):
    """
    Extract string with dimensions from bs4
    """
    dimensions_list = []
    for y in dimension_info:
        y_info = [d.text
            for d in y.find_all(
                "span", {"class": "range-revamp-product-details__label"})
            ]
        dimensions_list.append(y_info)
    #removed 'Artikelnummer:' string from lists in list.
    return [[i for i in x if i!='Artikelnummer:'] for x in dimensions_list]

def prepare_unique_list_of_lists(dimensions_list):
    """
    Filter out only unique string lists from list of lists
    """
    unique_dimensions_list = []
    for x in dimensions_list:
        if x not in unique_dimensions_list:
            unique_dimensions_list.append(x)
    return unique_dimensions_list


def inch_to_cm(dimension):
    "Recalculate inch to cm"
    for k,v in dimension.items():
        if k in ['width','height','length']:
            v*2.54
            dimension[k] = v*2.54
    return dimension


def create_dict_with_dimensions(product_features):
    """
    Extract features from string and save it in dict
    with following keys ['width','high','length','weight','packages']
    """
    info_dict = {}
    for info in product_features:
        info_item = info.split()
        for i, x in enumerate(info_item):
            try:
                float(x)
                info_dict[info_item[0]] = float(info_item[1])
            except:
                pass
    return info_dict

def create_dict_rename_keys(info_dict):
    """
    create dict and rename keys from every langauge to english
    """
    
    columns_name = ["width", "height", "length", "weight", "packages"]
    
    info_not_all_dimensions_given = {}
    if len(info_dict) == 4:
        info_not_all_dimensions_given[columns_name[0]] = list(info_dict.values())[0]
        info_not_all_dimensions_given[columns_name[1]] = list(info_dict.values())[2]
        info_not_all_dimensions_given[columns_name[2]] = list(info_dict.values())[2]
        info_not_all_dimensions_given[columns_name[3]] = list(info_dict.values())[1]
        info_not_all_dimensions_given[columns_name[4]] = list(info_dict.values())[3]
        return info_not_all_dimensions_given
    info_dict = {x: y for x, y in zip(columns_name, info_dict.values())}
    return info_dict

def recalculate_inch_to_cm(product_features):
    """
    check if 'cm' in product features. If not recalculate to cm
    """
    
    info_dict = create_dict_with_dimensions(product_features)
    # prepare dict for product with only 2 dimensions
    if any(['cm' in x for x in product_features]):
        info_dict = create_dict_rename_keys(info_dict)
        return info_dict
    else:
        info_dict = create_dict_rename_keys(info_dict)
        return inch_to_cm(info_dict)
    

def packages_dimensions_weight_to_df(unique_dimensions_list , number, product_name):
    """
    Create data frame all information about articles
    """
    # create empty list
    list_of_products = []
    # create empty dict
    product_info = {}
 
    # extract subarticle code and parameters for all subproducts in product
    for i, (x, y) in enumerate(zip(number, unique_dimensions_list)):
        # append to dict
        
        print(y)
        product_info = recalculate_inch_to_cm(y)
        product_info["subarticle_code"] = x.text.replace(".", "")
        product_info["product_name"] = product_name
        # append to list
        list_of_products.append(product_info)
    return pd.DataFrame(list_of_products)





def df_to_list(df, article_code):
    """
    Prepare output for API from data frame.
    [(
    article_code (str),
    item_count (int),
        [(
        package_id (int),
        package_length (int),
        package_width (int),
        package_height (int),
        package_weight (float)
        )]
    )]
    """
    # Initialize empty list
    return_list = []

    # Loop over each article
    for article, article_count in article_code.items():
        # Sub-list when there are multiple packages
        package_list = []
        # Find all matches in dataframe
        matched_packages = df[df["article_code"] == article]
        # Loop over all packages
        package_count = 1
        for _, matched_package in matched_packages.iterrows():
            # If the same package exists multiple times this will run more than once
            for idx in range(int(matched_package["packages"])):
                package_list.append(
                    (
                        package_count,
                        int(matched_package["height"]),
                        int(matched_package["width"]),
                        int(matched_package["length"]),
                        matched_package["weight"],
                    )
                )
                # Append package ID, dimensions and weight
                package_count += 1
        # Append list of packages
        return_list.append([article, article_count, package_list])
    return return_list


def get_local_data(path_to_csv):
    # Read and return data
    return pd.read_csv(PROJECT_DIR / PROJECT_NAME / path_to_csv, dtype=DTYPE_DICT)

def product_info_and_update_csv_database(
    article_dict, db, path_to_csv=DATABASE_PATH, item_count=1, lang_code="de1"
):
    """
    Check if article exists in database, if not scrap it and update
    Returns:
        return_list - list required for optimizer
        product_names - pd.dataframe containing article_code & product_name
    """
    # Only use article keys here
    article_code = [*article_dict]

    # Get data from either cloud or locally
    if db == "cloud":
        ikea_database = get_cloud_data(path_to_csv)
    else:
        ikea_database = get_local_data(path_to_csv)

    # Reduce size
    ikea_database = ikea_database.astype(IKEA_DATABASE_DTYPES)
    all_ordered_product_df = pd.DataFrame()
    new_product_for_database = pd.DataFrame()
    return_list = []

    for i, x in enumerate(article_code):
        # If article exists in database already
        if ikea_database.shape[0] > 0 and (ikea_database["article_code"] == x).any():
            all_ordered_product_df = all_ordered_product_df.append(
                ikea_database[ikea_database["article_code"] == x]
            )
        # If not
        else:
            # prepare url
            # lang_code[:2] removes numbers (i.e. de1 > de)...
            # ... Assumes all language codes are 2 characters
            url = prepare_url(x,
                              country_domain=IKEA_COUNTRY_DOMAIN[lang_code],
                              website_language=lang_code[:2])

            # check if item exists, if not return error
            html = check_if_item_exists(url)
            if html == WEBSITE_UNAVAILABLE:
                return WEBSITE_UNAVAILABLE
            html = scrape_product(url)
            if html == ARTICLE_NOT_FOUND:
                return ARTICLE_NOT_FOUND
            info, number, product_name = extract_inforamtion_from_html(html)
            dimensions_list = extract_dimensions_from_bs4(info)
            unique_dimensions_list = prepare_unique_list_of_lists(dimensions_list)
            df = packages_dimensions_weight_to_df(unique_dimensions_list , number, product_name)
            df["article_code"] = x
            all_ordered_product_df = all_ordered_product_df.append(df).astype(
                IKEA_DATABASE_DTYPES
            )
            new_product_for_database = new_product_for_database.append(df)

    product_names = all_ordered_product_df[["article_code", "product_name"]].drop_duplicates().set_index(
        ["article_code"]
    )

    return_list = df_to_list(all_ordered_product_df, article_dict)
    # Append new items and reduce size
    ikea_database = ikea_database.append(new_product_for_database).astype(
        IKEA_DATABASE_DTYPES
    )

    # Write to csv
    if db == "cloud":
        write_file = send_cloud_data(ikea_database, path_to_csv)
        if write_file != True:
            # TODO
            return "Error writing to file"
    else:
        ikea_database.to_csv(PROJECT_DIR / PROJECT_NAME / path_to_csv, index=False)

    return return_list, product_names
