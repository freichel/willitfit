import streamlit as st
import requests
from willitfit.app_utils.pdf_parser import pdf_to_dict
from willitfit.app_utils.form_transformer import form_to_dict
from willitfit.app_utils.trunk_dimensions import get_volume_space
from willitfit.app_utils.utils import get_data, gen_make_dict, gen_make_list
import pandas as pd
import os
from pathlib import Path

#import plotly.graph_objects as go
MY_URL = ""


def main():
    st.write(os.path.join(os.path.abspath(os.getcwd()), 'app_utils', 'cars_clean.csv')
    # # Render initial app instructions
    # with open('app_instructions.md', 'r') as f:
    #     contents = f.read()
    #     st.header(contents)

    # # Sidebar
    # st.sidebar.markdown("""
    #     ## Enter your data:
    #     """)

    # # Car model selector
    # car_make = st.sidebar.selectbox(
    #     'Select car brand:', 
    #     MAKE_LIST
    #     )
    # if car_make:
    #     car_model = st.sidebar.selectbox(
    #     'Select model:',
    #     MAKE_DICT[car_make]
    #     )
    # st.sidebar.markdown("""
    #     ---
    #     """)

    # # Upload pdf
    # uploaded_pdf = st.sidebar.file_uploader('(Recommended) On the IKEA website, export your wishlist as a PDF and upload it here:')
    # st.sidebar.markdown("""
    #     or
    #     """)

    # # Article number list
    # form = st.sidebar.form('Add your items individually:')
    # articles_list = form.text_area(
    #     'List your Article Numbers:', 
    #     help='Delimited by commas. If more than 1 of the same article, denote in brackets as shown. Format: XXX.XXX.XX (>1), '
    #     )
    # form.form_submit_button('Submit your list')

    # st.sidebar.markdown("""
    #     Click 'Generate' below!
    #     ---
    #     """)



    # ## Generate plot
    # if st.sidebar.button('Generate'):
    #     # Parsing uploaded_pdf to dict_ to POST
    #     if uploaded_pdf:
    #         dict_ = pdf_to_dict(uploaded_pdf)
    #         dict_['vol'] = get_volume_space(car_model, data=car_data)
    #         response = requests.post(MY_URL, dict_)

    #     # Build dict_ from form to POST
    #     if articles_list:
    #         dict_ = form_to_dict(articles_list)
    #         dict_['vol'] = get_volume_space(car_model, data=car_data)
    #         response = requests.post(MY_URL, dict_)

# response = requests.post(MY_URL, df)
# response_dict = response.json()

    # if response.status_code == 200:
    #     print("API call success")
    #     if response_dict['Viable'] == 1:
    #         st.write("Yes, it all fits perfectly!")
    #         # Gen plot
    #     elif response_dict['Viable'] == 2:
    #         st.write("Plenty of space left!")
    #         # Gen plot
    #     elif response_dict['Viable'] == 0:
    #         st.write("Too many items! Remove items from cart.")
    # else:
    #     print("API call error")
    #     st.error('Error')


# # Cached data retrieval function
# @st.cache
# def get_plotly_data():
#     print('get_plotly_data called')
#     z_data = pd.read_csv('trunk_filled')
#     z = z_data.values
#     sh_0, sh_1 = z.shape
#     x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
#     return x, y, z

# # Call retrieval function
# x, y, z = get_plotly_data()

# fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
# fig.update_layout(title='Optimised Trunk', autosize=False, width=800, height=800, margin=dict(l=40, r=40, b=40, t=40))

# # Plot
# st.plotly_chart(fig)

if __name__ == "__main__":
    main()