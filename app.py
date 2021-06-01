import streamlit as st
import requests
from willitfit.app_utils.pdf_parser import pdf_to_df
from willitfit.app_utils.form_transformer import form_to_df
import pandas as pd

#import plotly.graph_objects as go


MY_URL = ""
catalog = []
trunk_sizes = {'Generic Sedan': 0.4, 'Generic Hatchback': 0.3, 'Generic Compact SUV': 0.4, 'Generic Mid-size SUV': 0.5}
generic_cars = ['Generic Sedan', 'Generic Hatchback', 'Generic Compact SUV', 'Generic Mid-size SUV']

# Render initial app instructions
with open('app_instructions.md', 'r') as f:
    contents = f.read()
    st.header(contents)

# Sidebar
st.sidebar.markdown("""
    ## Enter your data:
    """)

# Car model selector
car_model = st.sidebar.selectbox(
    'Select car model:', 
    generic_cars
    )
st.sidebar.markdown("""
    ---
    """)

# Upload pdf
uploaded_pdf = st.sidebar.file_uploader('(Recommended) On the IKEA website, export your wishlist as a PDF and upload it here:')
st.sidebar.markdown("""
    or
    """)

# Article number list
form = st.sidebar.form('Add your items individually:')
articles_list = form.text_area(
    'List your Article Numbers:', 
    help='Delimited by commas. If more than 1 of the same article, denote in brackets as shown. Format: XXX.XXX.XX (>1), '
    )
form.form_submit_button('Submit your list')

st.sidebar.markdown("""
    ---
    """)



## Generate plot
st.sidebar.button('Generate')
# Parsing uploaded_pdf to POST
if uploaded_pdf:
    df = pdf_to_df(uploaded_pdf)

# Build df from form to POST
if articles_list:
    df = form_to_df(articles_list)
    
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