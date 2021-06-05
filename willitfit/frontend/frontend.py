import streamlit as st
from willitfit.app_utils.pdf_parser import pdf_to_dict
from willitfit.app_utils.form_transformer import form_to_dict
from willitfit.app_utils.trunk_dimensions import get_volume_space
from willitfit.app_utils.utils import gen_make_dict, gen_make_list
from willitfit.params import IKEA_WEBSITE_LANGUAGE, IKEA_COUNTRY_DOMAIN, CAR_DATABASE, NO_DATA_PROVIDED, ERRORS_SCRAPER, ERRORS_OPTIMIZER, PROJECT_NAME, PROJECT_DIR, DATA_FOLDER, INTERFACE_INSTRUCTIONS
from willitfit.app_utils.googlecloud import get_cloud_data
from willitfit.optimizers.volumeoptimizer import generate_optimizer
from willitfit.scrapers.IKEA import product_info_and_update_csv_database
from willitfit.plotting.plotter import plot_all
import plotly
#import pandas as pd
import numpy as np

# Get car data from cloud CSV file
data = get_cloud_data(DATA_FOLDER+"/"+CAR_DATABASE)
MAKE_LIST = gen_make_list(data)
MAKE_DICT = gen_make_dict(data)

def main():
    # Render initial app instructions
    with open(PROJECT_DIR/PROJECT_NAME/INTERFACE_INSTRUCTIONS, 'r') as f:
        contents = f.read()
        st.header(contents)

    # Sidebar
    st.sidebar.markdown("""
        #### Enter your data:
        """)

    # Car model selector
    car_make = st.sidebar.selectbox(
        'Select car brand:',
        MAKE_LIST
        )
    if car_make:
        car_model = st.sidebar.selectbox(
        'Select model:',
        MAKE_DICT[car_make]
        )
    st.sidebar.markdown("""
        ---
        """)

    # Upload pdf
    uploaded_pdf = st.sidebar.file_uploader('Upload PDF:')
    st.sidebar.markdown("""
        ##### or
        """)

    # Article number list
    form = st.sidebar.form('Add your items manually:')
    articles_str = form.text_area(
        'List your Article Numbers:',
        help='Delimited by commas. If more than 1 of the same article, denote in brackets as shown. Format: XXX.XXX.XX (>1), ',
        value="904.990.66 (2)"
        )
    form.form_submit_button('Submit your list')

    plot_unavailable = st.sidebar.checkbox('Show unavailable space')

    st.sidebar.markdown("""
        Click 'Generate' below!
        ---
        """)

    ## Generate plot
    if st.button('Generate'):
        st.write("Unpacking data...")
        # Parsing uploaded_pdf to dict_
        if uploaded_pdf:
            article_dict = pdf_to_dict(uploaded_pdf, IKEA_WEBSITE_LANGUAGE)
        # Build dict_ from form
        elif articles_str:
            article_dict = form_to_dict(articles_str)
        # If not data was provided, break
        else:
            st.error(NO_DATA_PROVIDED)
            st.stop()

        # Find car trunk dimensions for given car_id
        st.write("Getting trunk volume...")
        volume_space = get_volume_space(car_model)

        # Call scraper with article list and website location/language.
        # Receive list of package dimensions and weights for each article.

        st.write("Browsing IKEA for you...")
        scraper_return = product_info_and_update_csv_database(article_dict)

        if scraper_return not in ERRORS_SCRAPER:
            article_list = scraper_return
        else:
            st.error(scraper_return)
            st.stop()

        # Call optimizer with article list and volume array.
        # Receive package coordinates and filled volume array.

        st.write("Stacking packages...")
        optimizer_return = generate_optimizer(article_list, np.copy(volume_space), generator_random_lists=10, optimizer_max_attempts=10)
        if optimizer_return not in ERRORS_OPTIMIZER:
            filled_space, package_coordinates = optimizer_return
        else:
            st.error(optimizer_return)
            st.stop()

        # Call plotter with package coordinates and filled volume array.
        # Receive plot

        st.write("Solution found! Visualisation loading...")
        plotter_return = plot_all(filled_space, package_coordinates, plot_unavailable=plot_unavailable)
        st.plotly_chart(plotter_return)

if __name__ == "__main__":
    main()
