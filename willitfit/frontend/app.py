import streamlit as st
import requests
from willitfit.app_utils.pdf_parser import pdf_to_dict
from willitfit.app_utils.form_transformer import form_to_dict
from willitfit.app_utils.utils import gen_make_dict, gen_make_list
from willitfit.params import LANG_CODE, IKEA_WEBSITE_LANGUAGE, IKEA_COUNTRY_DOMAIN, API_URL, CAR_DATABASE, NO_DATA_PROVIDED, ERRORS_SCRAPER, ERRORS_OPTIMIZER, PROJECT_NAME, PROJECT_DIR, DATA_FOLDER, INTERFACE_INSTRUCTIONS
from willitfit.app_utils.googlecloud import get_cloud_data
import pandas as pd
import os
from pathlib import Path
import plotly
import json

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

    ## Generate plot
    if st.button('Generate'):
        # Parsing uploaded_pdf to dict_ to POST
        if uploaded_pdf:
            dict_ = pdf_to_dict(uploaded_pdf, LANG_CODE[pdf_lang])
            params = {
                "article_dict": dict_,
                "car_model": car_model,
                "IKEA_country": IKEA_COUNTRY_DOMAIN,
                "IKEA_language": IKEA_WEBSITE_LANGUAGE
                    }

            response = requests.post(API_URL, json=params)

        # Build dict_ from form to POST
        elif articles_str:
            dict_ = form_to_dict(articles_str)
            params = {
                "article_dict": dict_,
                "car_model": car_model,
                "IKEA_country": IKEA_COUNTRY_DOMAIN,
                "IKEA_language": IKEA_WEBSITE_LANGUAGE
                    }
            response = requests.post(API_URL, json=params)

        else:
            st.error(NO_DATA_PROVIDED)

        if response.status_code == 200:
            return_val = response.text

            # Scraper error
            if return_val.strip("\"") in ERRORS_SCRAPER:
                st.error(return_val.strip("\""))
                st.stop()
            # Optimizer error
            if return_val.strip("\"") in ERRORS_OPTIMIZER:
                st.error(return_val.strip("\""))
                st.stop()
            # Successful
            st.write("Solution found! Visualisation loading...")
            st.plotly_chart(plotly.io.from_json(json.loads(return_val)))
        else:
            st.error(f"Unspecified error {response.status_code}")
            st.stop()

if __name__ == "__main__":
    main()
