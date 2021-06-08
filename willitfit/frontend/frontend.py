import streamlit as st
from willitfit.app_utils.pdf_parser import pdf_to_dict
from willitfit.app_utils.form_transformer import form_to_dict
from willitfit.app_utils.trunk_dimensions import get_volume_space
from willitfit.app_utils.utils import gen_make_dict, gen_make_list
from willitfit.params import (
    OPT_MAX_ATTEMPTS,
    RANDOM_LIST_COUNT,
    CAR_DATABASE,
    NO_DATA_PROVIDED,
    ERRORS_SCRAPER,
    ERRORS_OPTIMIZER,
    PROJECT_NAME,
    PROJECT_DIR,
    DATA_FOLDER,
    INTERFACE_INSTRUCTIONS,
    LANG_CODE,
    CAR_MODEL_CHOOSE,
    CAR_BRAND_CHOOSE,
    LANG_CHOOSE,
)
from willitfit.app_utils.googlecloud import get_cloud_data
from willitfit.optimizers.volumeoptimizer import generate_optimizer
from willitfit.scrapers.IKEA import product_info_and_update_csv_database
from willitfit.plotting.plotter import plot_all
import plotly
import numpy as np
import time

# Get car data from cloud CSV file
data = get_cloud_data(DATA_FOLDER + "/" + CAR_DATABASE)
MAKE_LIST = gen_make_list(data)
MAKE_DICT = gen_make_dict(data)

icon = str(PROJECT_DIR / "resources/icon.jpeg")
st.set_page_config(page_title="Will It Fit?", page_icon=icon, layout="wide")


class LanguageSelector:
    def __init__(self):
        self.lang = LANG_CHOOSE

    def show_page(self):
        # Dropdown for language
        self.lang = st.selectbox(
            "Select your local IKEA website language:", [*LANG_CODE], index=0
        )


class CarSelector:
    def __init__(self):
        self.car_model = "---Choose a model---"

    def show_page(self):
        # Car model selector
        car_make = st.selectbox("Select car brand:", MAKE_LIST)
        if car_make:
            car_model = st.selectbox(
                "Select model:", MAKE_DICT.get(car_make, [CAR_MODEL_CHOOSE])
            )
        # TODO
        # Display car image

        self.car_model = car_model


class ArticlePicker:
    def __init__(self):
        self.article_dict = {}

    def show_page(self):
        
        pdf_col, num_art_col= st.beta_columns(2)
        # Upload pdf
        uploaded_pdf = pdf_col.file_uploader("Upload PDF:")
        ## PDF instructions expandable
        instr_expander = pdf_col.beta_expander("Expand for instructions")
        with instr_expander:
            with open(PROJECT_DIR / PROJECT_NAME / INTERFACE_INSTRUCTIONS, "r") as f:
                contents = f.read()
                st.write(contents)
        # Number of article to pack
        form = num_art_col.form('forma')
        num_str = form.text_area(
            "Alternatively, list your Article Numbers:",
            help="Between 1 and inf ",
            value="1",
        )
        form.form_submit_button('Submit number of articles to pack')

        #####
        with st.form('columns_in_forma'): 
            article_s = []
            i = 0
            while i < int(num_str):
                
                
                _, manual_col, amount_col= st.beta_columns([3,1.5,1.5])
    
                # Article number list
                articles_str = manual_col.text_area(
                    "Product ID:",
                    help="Delimited by commas. Format: XXX.XXX.XX , ",
                    value="904.990.66",
                    key = str(i))
                # Amount
                amount_str = amount_col.text_area(
                    "Amount:",
                    help="Between 1 and inf ",
                    value="1",
                    key = str(i))
                i+=1
        form.form_submit_button('Submit information about articles')
            
        # Columns
        # pdf_col, manual_col= st.beta_columns(2)
        # # Upload pdf
        # uploaded_pdf = pdf_col.file_uploader("Upload PDF:")
        # ## PDF instructions expandable
        # instr_expander = pdf_col.beta_expander("Expand for instructions")
        # with instr_expander:
        #     with open(PROJECT_DIR / PROJECT_NAME / INTERFACE_INSTRUCTIONS, "r") as f:
        #         contents = f.read()
        #         st.write(contents)
        # # Article number list
        # articles_str = manual_col.text_area(
        #     "Alternatively, list your Article Numbers:",
        #     help="Delimited by commas. If more than 1 of the same article, denote in brackets as shown. Format: XXX.XXX.XX (>1), ",
        #     value="904.990.66 (2)",
        # )
        
        cols = st.beta_columns([5, 1, 5])

        if cols[1].button("Generate"):
            # Status message field wich will get overwritten
            unpack_message = st.empty()
            unpack_message.info("Unpacking data...")
            # Parsing uploaded_pdf to article_dict
            if uploaded_pdf:
                self.article_dict = pdf_to_dict(uploaded_pdf, LANG_CODE[pdf_lang])
                unpack_message.success("Articles extracted from PDF.")
            # Or build article_dict from form
            elif articles_str:
                self.article_dict = form_to_dict(articles_str)
                unpack_message.success("Articles extracted from form.")
            else:
                unpack_message.error(NO_DATA_PROVIDED)
                st.stop()


# Individual elements to be displayed sequentially
# TODO
# They're labelled "pages" because ideally we'd use individual pages. However, haven't gotten there yet.
pages = {
    "select_lang": LanguageSelector,
    "select_car": CarSelector,
    "pick_art": ArticlePicker,
}


def main():
    # Icon
    cols = st.beta_columns([2, 1, 2])
    cols[1].image(icon, use_column_width=True)

    # Language selection
    page = pages["select_lang"]()
    page.show_page()
    # Loop until a language is selected
    while page.lang == LANG_CHOOSE:
        status = st.empty()
        time.sleep(0.5)
    # Assign language
    pdf_lang = page.lang

    # Car selection
    page = pages["select_car"]()
    page.show_page()
    # Loop until a car is selected
    while page.car_model == CAR_MODEL_CHOOSE:
        status = st.empty()
        time.sleep(0.5)
    # Assign car model
    car_model = page.car_model

    # Article selection
    page = pages["pick_art"]()
    page.show_page()
    # Loop until articles are selected
    while page.article_dict == {}:
        status = st.empty()
        time.sleep(0.5)
    # Assign articles
    article_dict = page.article_dict

    # Find car trunk dimensions for given car_id
    trunk_message = st.empty()
    trunk_message.info(f"Getting trunk volume for your {car_model}...")
    volume_space = get_volume_space(car_model)
    trunk_message.success(f"Trunk volume for your {car_model} computed.")
    # Call scraper with article list and website location/language.
    # Receive list of package dimensions and weights for each article.

    scraper_message = st.empty()
    scraper_message.info("Browsing IKEA for you...")
    scraper_return = product_info_and_update_csv_database(article_dict)

    if scraper_return not in ERRORS_SCRAPER:
        article_list = scraper_return[0]
        product_names = scraper_return[1]
        scraper_message.success("All articles found on IKEA.")
    else:
        scraper_message.error(scraper_return)
        st.stop()

    # How many articles and packages are there in total?
    article_count = sum([article[1] for article in article_list])
    package_count = sum([len(article[2]) * article[1] for article in article_list])

    # Call optimizer with article list and volume array.
    # Receive package coordinates and filled volume array.
    optimizer_message = st.empty()
    optimizer_message.info(
        f"Running optimizer for {article_count} article{'s' if article_count>1 else ''} and {package_count} individual package{'s' if package_count>1 else ''}..."
    )
    optimizer_return = generate_optimizer(
        article_list,
        np.copy(volume_space),
        generator_random_lists=RANDOM_LIST_COUNT,
        optimizer_max_attempts=OPT_MAX_ATTEMPTS,
    )
    if optimizer_return not in ERRORS_OPTIMIZER:
        filled_space, package_coordinates = optimizer_return
    else:
        optimizer_message.error(optimizer_return)
        st.stop()
    optimizer_message.success(
        f"Solution found for {article_count} article{'s' if article_count>1 else ''} and {package_count} individual package{'s' if package_count>1 else ''}."
    )

    # Call plotter with package coordinates and filled volume array.
    # Receive plot
    plotter_message = st.empty()
    plotter_message.info("Building 3D plot")
    plotter_return = plot_all(filled_space, package_coordinates, product_names)

    st.plotly_chart(plotter_return, use_container_width=True)
    plotter_message.empty()


if __name__ == "__main__":
    main()
