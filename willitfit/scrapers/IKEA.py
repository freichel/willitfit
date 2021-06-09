"""
Receives list of article codes and article counts.
Scrapes IKEA website to obtain package dimensions (rounded up to next cm), weights (in kg rounded up 2 decimals) and counts.
Returns list of package dimensions and weights.
"""

from willitfit.params import (
    IKEA_COUNTRY_DOMAIN,
    IKEA_WEBSITE_LANGUAGE,
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

import time
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


def scrape_product(
    article_code,
    country_domain=IKEA_COUNTRY_DOMAIN,
    website_language=IKEA_WEBSITE_LANGUAGE,
):
    """
    Scrape the artikle from Ikea website
    Filter out part of the site with important informations.
    When we run the test first time,
    latest version of chromedriver binary is downloaded and saved in cache
    and it is reused every time we run tests.
    If your browser auto updates the version,
    then the respective chromedriver is auto downloaded
    and updated when running tests.
    """
    # Ikea url
    IKEA_URL = f"https://www.ikea.com/{country_domain}/{website_language}/"
    IKEA_SEARCH_URL = f"search/products/?q="
    # Request to check if website exsist, if not return str
    r = requests.get(os.path.join(IKEA_URL, IKEA_SEARCH_URL, article_code))
    if r.status_code == 404:
        return WEBSITE_UNAVAILABLE
    # Scrap website and select relevant part of the website
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_settings()
    )
    driver.get(os.path.join(IKEA_URL, IKEA_SEARCH_URL, article_code))
    try:
        important_part_of_page = driver.find_element_by_class_name("results__list")
        # Check if the article exists, if not return str
        tag = important_part_of_page.find_element_by_tag_name("a")
    except:
        return ARTICLE_NOT_FOUND
    # if article exists return important part of page
    # https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen
    driver.execute_script("arguments[0].click();", tag)
    
    time.sleep(30)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    important_part_of_page = soup.find_all(
        "div", {"id": "SEC_product-details-packaging"}
    )
    print(important_part_of_page[0])
    return important_part_of_page[0]

def inch_to_cm(d):
    for k,v in d.items():
        if k in ['width','height','length']:
            v*2.54
            d[k] = v*2.54
    return d

def extract_numeric_product_to_dict(product_features):
    """
    Extract features from string and save it in dict
    with following keys ['width','high','length','weight','packages']
    """
    info_dict = {}
    new_columns_name = ["width", "height", "length", "weight", "packages"]
    for info in product_features:
        info_item = info.split()
        for i, x in enumerate(info_item):
            try:
                float(x)
                info_dict[info_item[0]] = float(info_item[1])
            except:
                pass
    # prepare dict for product with only 2 dimensions
    if any(['cm' in x for x in product_features]):
        info_not_all_dimensions_given = {}
        if len(info_dict) == 4:
            info_not_all_dimensions_given[new_columns_name[0]] = list(info_dict.values())[0]
            info_not_all_dimensions_given[new_columns_name[1]] = list(info_dict.values())[2]
            info_not_all_dimensions_given[new_columns_name[2]] = list(info_dict.values())[2]
            info_not_all_dimensions_given[new_columns_name[3]] = list(info_dict.values())[1]
            info_not_all_dimensions_given[new_columns_name[4]] = list(info_dict.values())[3]
            return info_not_all_dimensions_given
        info_dict = {x: y for x, y in zip(new_columns_name, info_dict.values())}
        return info_dict
    else:
        info_not_all_dimensions_given = {}
        if len(info_dict) == 4:
            info_not_all_dimensions_given[new_columns_name[0]] = list(info_dict.values())[0]
            info_not_all_dimensions_given[new_columns_name[1]] = list(info_dict.values())[2]
            info_not_all_dimensions_given[new_columns_name[2]] = list(info_dict.values())[2]
            info_not_all_dimensions_given[new_columns_name[3]] = list(info_dict.values())[1]
            info_not_all_dimensions_given[new_columns_name[4]] = list(info_dict.values())[3]
            return inch_to_cm(info_not_all_dimensions_given)
        info_dict = {x: y for x, y in zip(new_columns_name, info_dict.values())}
        return inch_to_cm(info_dict)


def packages_dimensions_weights(page):
    """
    Create data frame with information about subarticles
    """
    # filter out important info with beautiful soup
    info = page.find_all("div", {"class": "range-revamp-product-details__container"})
    number = page.find_all("span", {"class": "range-revamp-product-identifier__value"})
    product_name = page.find_all(
        "span", {"class": "range-revamp-product-details__header notranslate"}
    )[0].text
    # create empty list
    list_of_products = []
    # create empty dict
    product_info = {}
    # extract subarticle code and parameters for all subproducts in product
    for i, (x, y) in enumerate(zip(number, info)):
        y_info = [
            info.text
            for info in y.find_all(
                "span", {"class": "range-revamp-product-details__label"}
            )
        ]
        # append to dict
        product_info = extract_numeric_product_to_dict(y_info)
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


def product_info_and_update_csv_database(
    article_dict, path_to_csv=DATABASE_PATH, item_count=1
):
    """
    Check if article exists in database, if not scrap it and update
    Returns:
        return_list - list required for optimizer
        product_names - pd.dataframe containing article_code & product_name
    """
    # Only use article keys here
    article_code = [*article_dict]

    ikea_database = get_cloud_data(path_to_csv)
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
            page = scrape_product(
                x,
                country_domain=IKEA_COUNTRY_DOMAIN,
                website_language=IKEA_WEBSITE_LANGUAGE,
            )
            if page == WEBSITE_UNAVAILABLE:
                return WEBSITE_UNAVAILABLE
            if page == ARTICLE_NOT_FOUND:
                return ARTICLE_NOT_FOUND
            df = packages_dimensions_weights(page)
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
    write_file = send_cloud_data(ikea_database, path_to_csv)
    if write_file != True:
        # TODO
        return "Error writing to file"
    return return_list, product_names


