import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Scrape uri from each page
## Populate uri_list
uri_list = []

BASE_URL = (
    "http://www.ridc.org.uk/features-reviews/out-and-about/choosing-car/car?page="
)
MAX_PAGE = 157

## Pagination
for page in range(1, MAX_PAGE + 1):
    print(f"Parsing page {page}...")

    PAGE_URL = BASE_URL + f"{page}"
    response = requests.get(PAGE_URL)
    page_soup = BeautifulSoup(response.content, "html.parser")

    for item in page_soup.find_all(
        class_="views-field views-field-title views-align-left"
    ):
        uri_list.append(item.find("a").attrs["href"])


# Scrape through every uri
SCRAPE_BASE_URL = "http://www.ridc.org.uk"

## Compile regex to parse numerical fields
rx = re.compile(r"(\d*)mm")
# Access every uri
df_dict = {
    "make": [],
    "car_model": [],
    "depth": [],
    "height": [],
    "width": [],
    "extra_depth": [],
    "img_url": [],
}
for uri in uri_list:
    PAGE_URL = SCRAPE_BASE + f"{uri}"
    response = requests.get(PAGE_URL)
    page_soup = BeautifulSoup(response.content, "html.parser")

    car_model = page_soup.find("h1").text
    make = page_soup.find(class_="field--name-field-make").find("a").text
    depth = int(
        int(
            rx.findall(
                page_soup.find(
                    class_="field--name-field-length-of-boot-floor-back"
                ).text
            )[0]
        )
        / 10
    )
    height = int(
        int(
            rx.findall(
                page_soup.find(
                    class_="field--name-field-vertical-height-of-boot-op"
                ).text
            )[0]
        )
        / 10
    )
    width = int(
        int(
            rx.findall(
                page_soup.find(
                    class_="field--name-field-width-of-boot-floor-at-nar"
                ).text
            )[0]
        )
        / 10
    )
    try:
        extra_depth = int(
            int(
                rx.findall(
                    page_soup.find(
                        class_="field field--name-field-length-of-boot-floor-back- field--type-integer field--label-inline"
                    )
                    .find(class_="field__item")
                    .contents[0]
                )[0]
            )
            / 10
        )
    except AttributeError:
        extra_depth = depth

    try:
        img_url = SCRAPE_BASE + (page_soup.find("picture").find("img").attrs["src"])
    except AttributeError:
        img_url = None

    df_dict["make"].append(make)
    df_dict["car_model"].append(car_model)
    df_dict["depth"].append(depth)
    df_dict["height"].append(height)
    df_dict["width"].append(width)
    df_dict["extra_depth"].append(extra_depth)
    df_dict["img_url"].append(img_url)

data = pd.DataFrame(df_dict)
# Clean data
data["car_model"] = data["car_model"].str.replace("\n", "")
## Optional: Make model names upper case
data["car_model"] = data["car_model"].str.upper()

## Function for removing duplicated 'make' names in 'car_model' and strip trailing whitespace
def remove_make(df):
    make = df["make"].upper()
    if make in df["car_model"]:
        df["car_model"] = df["car_model"].replace(make, "").strip()
    return df


data = data.apply(remove_make, axis=1)

## Drop Duplicates
data.drop(index=data[data["car_model"].duplicated()].index, inplace=True)

## Fix models with missing configs:
data.at[58, 'car_model'] = '911 CARRERA CABRIOLET 2DR CONVERTIBLE 2016'
data.at[394, 'car_model'] = 'CITROEN NEMO 1.4 XLS 5DR MPV 2008'
data.at[1196, 'car_model'] = 'PEUGEOT BIPPER 75 5DR MPV 2008'
data.at[1368, 'car_model'] = 'SEAT IBIZA ECOMOTIVE 1.4 TDI 5DR HATCH 2009'

## Function for creating 'config' column
def create_generic_config(df):
    CAR_CONFIGURATIONS = {
        '4X4': 'BOXY', 
        'CONVERTIBLE': 'BOXY', 
        'COUPE': 'BOXY', 
        'ESTATE': 'BOXY', 
        'HATCH': 'SLANT', 
        'MPV': 'BOXY', 
        'SALOON': 'BOXY'
    }
    for CONFIG in [*CAR_CONFIGURATIONS]:
        if CONFIG in df["car_model"]:
            df["generic_config"] = CAR_CONFIGURATIONS[CONFIG]
    return df

data = data.apply(create_generic_config, axis=1)

## Export as csv
data.to_csv("cars_clean.csv", index=False)
