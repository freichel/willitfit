import streamlit as st
from willitfit.app_utils.pdf_parser import pdf_to_dict
from willitfit.app_utils.form_transformer import form_to_dict
from willitfit.app_utils.trunk_dimensions import get_volume_space
from willitfit.app_utils.utils import gen_make_dict, gen_make_list
from willitfit.params import IKEA_WEBSITE_LANGUAGE, IKEA_COUNTRY_DOMAIN, OPT_MAX_ATTEMPTS, RANDOM_LIST_COUNT, CAR_DATABASE, NO_DATA_PROVIDED, ERRORS_SCRAPER, ERRORS_OPTIMIZER, PROJECT_NAME, PROJECT_DIR, DATA_FOLDER, INTERFACE_INSTRUCTIONS, LANG_CODE
from willitfit.app_utils.googlecloud import get_cloud_data
from willitfit.optimizers.volumeoptimizer import generate_optimizer
from willitfit.scrapers.IKEA import product_info_and_update_csv_database
from willitfit.plotting.plotter import plot_all
import plotly
import numpy as np



# Get car data from cloud CSV file
data = get_cloud_data(DATA_FOLDER+"/"+CAR_DATABASE)
MAKE_LIST = gen_make_list(data)
MAKE_DICT = gen_make_dict(data)

icon = PROJECT_DIR/'resources/icon.jpeg'
st.set_page_config(page_title='Will It Fit?',page_icon = icon, layout = 'wide')
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
    pdf_lang = st.sidebar.selectbox('Select PDF language:', [*LANG_CODE])
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

    ## Generate plot
    if st.button('Generate'):
        st.info("Unpacking data...")
        # Parsing uploaded_pdf to dict_
        if uploaded_pdf:
            article_dict = dict_ = pdf_to_dict(uploaded_pdf, LANG_CODE[pdf_lang])
        # Build dict_ from form
        elif articles_str:
            article_dict = form_to_dict(articles_str)
        # If not data was provided, break
        else:
            st.error(NO_DATA_PROVIDED)
            st.stop()

        # Find car trunk dimensions for given car_id
        st.warning("Getting trunk volume...")
        volume_space = get_volume_space(car_model)

        # Call scraper with article list and website location/language.
        # Receive list of package dimensions and weights for each article.

        st.error("Browsing IKEA for you...")
        scraper_return = product_info_and_update_csv_database(article_dict)

        if scraper_return not in ERRORS_SCRAPER:
            article_list = scraper_return
        else:
            st.error(scraper_return)
            st.stop()

        # Call optimizer with article list and volume array.
        # Receive package coordinates and filled volume array.

        st.write("Stacking packages...")
        optimizer_return = generate_optimizer(article_list, np.copy(volume_space), generator_random_lists=RANDOM_LIST_COUNT, optimizer_max_attempts=OPT_MAX_ATTEMPTS)
        if optimizer_return not in ERRORS_OPTIMIZER:
            filled_space, package_coordinates = optimizer_return
        else:
            st.error(optimizer_return)
            st.stop()

        # Call plotter with package coordinates and filled volume array.
        # Receive plot

        st.write("Solution found! Visualisation loading...")
        plotter_return = plot_all(filled_space, package_coordinates, plot_unavailable=True)
        st.plotly_chart(plotter_return)

if __name__ == "__main__":
    main()
