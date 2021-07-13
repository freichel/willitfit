import sys
import streamlit as st
from willitfit.app_utils.pdf_parser import pdf_to_df, pdf_df_to_dict
from willitfit.app_utils.form_transformer import form_to_dict
from willitfit.app_utils.trunk_dimensions import get_volume_space
from willitfit.app_utils.utils import get_local_data, gen_make_dict, gen_make_list, get_image, dict_to_name_list
from willitfit.params import (
    BIAS_STACKS,
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
    OPTIMIZER_OPTIONS,
    STACKING_OPTIONS
)
from willitfit.app_utils.googlecloud import get_cloud_data
from willitfit.optimizers.volumeoptimizer import generate_optimizer
from willitfit.scrapers.IKEA import product_info_and_update_csv_database
from willitfit.plotting.plotter import plot_all
import plotly
import numpy as np
import time

# # Get car data from cloud CSV file
# data = get_cloud_data(DATA_FOLDER + "/" + CAR_DATABASE)
# MAKE_LIST = gen_make_list(data)
# MAKE_DICT = gen_make_dict(data)

class CarData:
    def __init__(self, db):
        self.data = self.get_car_data(db)
        self.make_list = gen_make_list(self.data)
        self.make_dict = gen_make_dict(self.data)

    def get_car_data(self, db):
        if db == "cloud":
            return get_cloud_data(DATA_FOLDER + "/" + CAR_DATABASE)
        else:
            return get_local_data(DATA_FOLDER + "/" + CAR_DATABASE)


icon = str(PROJECT_DIR / "resources/icon.png")
st.set_page_config(
    page_title="Will It Fit?",
    page_icon=icon,
    layout="wide"
    )

class LanguageSelector:
    def __init__(self):
        self.lang = LANG_CHOOSE

    def show_page(self):
        # Dropdown for language
        self.lang = st.selectbox(
            "Select your local IKEA website language:",
            [*LANG_CODE],
            index=0
            )

class CarSelector:
    def __init__(self):
        self.car_model = CAR_BRAND_CHOOSE

    def show_page(self, carDB):
        # Car model selector
        car_make = st.selectbox("Select car brand:", carDB.make_list)
        if car_make:
            car_model = st.selectbox(
            "Select model:",
            carDB.make_dict.get(car_make, [CAR_MODEL_CHOOSE])
            )
            if car_model is not CAR_MODEL_CHOOSE:
                car_cols = st.beta_columns([1,1,1])
                image_url = get_image(carDB.data, car_model)
                if type(image_url) is not float:
                    car_cols[1].image(image_url)
        self.car_model = car_model

class ArticlePicker:
    def __init__(self):
        self.article_dict = {}
        self.placeholder = "604.845.80 (10), 404.703.29 (15)"

    def show_page(self, pdf_lang):
        # Columns
        pdf_col, manual_col = st.beta_columns(2)
        # Upload pdf
        uploaded_pdf = pdf_col.file_uploader("Upload PDF:")
        ## PDF instructions expandable
        instr_expander = pdf_col.beta_expander("Expand for instructions")
        with instr_expander:
            with open(PROJECT_DIR / PROJECT_NAME / INTERFACE_INSTRUCTIONS, "r") as f:
                contents = f.read()
                st.write(contents)
        # Article number list
        ## Initial placeholder value
        articles_str = manual_col.text_area(
            "Alternatively, list your Article Numbers:",
            help="Delimited by commas. If more than 1 of the same article, denote in brackets as shown. Format: XXX.XXX.XX (>1), XXX.XX.XX ",
            value=f"{self.placeholder}"
            )
        ## Empty line space
        extra_line_empty = manual_col.empty()
        # extra_depth checkbox
        extra_depth = manual_col.checkbox(
                'Back-seat down/removed if applicable',
                value=False
                )
        self.extra_depth = extra_depth

        cols = st.beta_columns([1, 2, 1])
        expander = cols[1].beta_expander("Advanced Optimizer Settings")
        # TODO - please advise on the preferred style: .info or help. Or a mix, as currently implemented?
        self.optimizer_setting = expander.select_slider(label="Overall - You can further customize individual settings below.", options=list(OPTIMIZER_OPTIONS.keys()), value="Standard")
        expander.info(OPTIMIZER_OPTIONS[self.optimizer_setting][0])
        #TODO - cannot get the line break properly displayed in the help argument
        self.bias_setting = expander.select_slider(label="Stacking - How strictly will the optimizer attempt to place packages as flat as possible?", options=list(STACKING_OPTIONS.keys()), value=OPTIMIZER_OPTIONS[self.optimizer_setting][1], help=chr(10).join([f"{key}: {value[0]}" for key, value in list(STACKING_OPTIONS.items())]))
        self.random_list_setting = expander.number_input(label="Random lists - Increasing this might yield better results, but it will also take longer.", min_value=0, max_value=20, value=OPTIMIZER_OPTIONS[self.optimizer_setting][2])
        self.attempts_setting = expander.number_input(label="Number of attempts - When it runs out of space, the optimizer tries a new approach up to the defined number of attempts.", min_value=1, max_value=10, value=OPTIMIZER_OPTIONS[self.optimizer_setting][3])

        # Centering Generate button with columns
        cols = st.beta_columns([5,1,5])

        if cols[1].button("Will It Fit?"):
            # Status message field wich will get overwritten
            self.unpack_message = st.empty()
            self.unpack_message.info("Unpacking data...")
            # Parsing uploaded_pdf to article_dict
            if uploaded_pdf:
                pdf_return = pdf_to_df(uploaded_pdf, LANG_CODE[pdf_lang])
                if isinstance(pdf_return, str):
                    self.unpack_message.error(pdf_return)
                    st.stop()
                # Build article_dict from df
                self.article_dict = pdf_df_to_dict(pdf_return)
                self.unpack_message.success("Articles extracted from PDF.")

            # Or build article_dict from form
            elif articles_str:
                form_return = form_to_dict(articles_str)
                if isinstance(form_return, str):
                    self.unpack_message.error(form_return)
                    st.stop()
                self.article_dict = form_return
                self.unpack_message.success("Articles extracted from form.")
            else:
                self.unpack_message.error(NO_DATA_PROVIDED)
                st.stop()

# Individual elements to be displayed sequentially
# They're labelled "pages" because ideally we'd use individual pages. However, haven't gotten there yet.
pages = {
    "select_lang": LanguageSelector,
    "select_car": CarSelector,
    "pick_art": ArticlePicker,
}


def main(db="cloud"):
    # Icon
    cols = st.beta_columns([2, 1, 2])
    cols[1].image(icon, use_column_width=True)

    # Get car database
    CarDB = CarData(db)

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
    page.show_page(CarDB)
    # Loop until a car is selected
    while page.car_model == CAR_MODEL_CHOOSE:
        status = st.empty()
        time.sleep(0.5)
    # Assign car model
    car_model = page.car_model

    # Article selection
    page = pages["pick_art"]()
    page.show_page(pdf_lang)
    # Loop until articles are selected
    while page.article_dict == {}:
        status = st.empty()
        time.sleep(0.5)
    # Assign articles
    article_dict = page.article_dict

    # Assign optimizer settings
    bias_setting = BIAS_STACKS[STACKING_OPTIONS[page.bias_setting[1]][1]:STACKING_OPTIONS[page.bias_setting[0]][1]+1]
    RANDOM_LIST_COUNT = page.random_list_setting
    OPT_MAX_ATTEMPTS = page.attempts_setting


    # Toggle extra_depth
    extra_depth = page.extra_depth

    # Find car trunk dimensions for given car_model
    trunk_message = st.empty()
    trunk_message.info(f"Getting trunk volume for your {car_model}...")
    volume_space, trunk_dims = get_volume_space(
        CarDB.data,
        car_model,
        extra_depth=extra_depth
        )
    trunk_message.success(f"Trunk volume for your {car_model} computed.")
    st.success(f"Your trunk dimensions are {trunk_dims[0]}cm x {trunk_dims[1]}cm x {trunk_dims[2]}cm")

    # Call scraper with article list and website location/language.
    # Receive list of package dimensions and weights for each article.
    # Scraper function and feedback
    scraper_message = st.empty()
    scraper_message.info("Browsing IKEA for you...")

    scraper_return = product_info_and_update_csv_database(article_dict,db,lang_code=LANG_CODE[pdf_lang])

    if scraper_return not in ERRORS_SCRAPER:
        article_list = scraper_return[0]
        product_names = scraper_return[1]
        scraper_message.success("All articles found on IKEA:")
        st.success(dict_to_name_list(article_dict, product_names))
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
        bias_options=bias_setting
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
    plotter_message.info("Building 3D plot...")
    plotter_return = plot_all(filled_space, package_coordinates, product_names)
    st.plotly_chart(plotter_return, use_container_width=True)
    plotter_message.empty()
    # Clean up messages
    plotter_message.success("YES! IT FITS!")
    optimizer_message.empty()
    scraper_message.empty()
    trunk_message.empty()
    page.unpack_message.empty()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
