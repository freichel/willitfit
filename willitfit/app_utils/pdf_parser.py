"""
Utilities for parsing article numbers and units of articles from IKEA wishlist PDF's
"""

from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from willitfit.params import NOT_PDF, UNABLE_TO_PARSE_LANG
import re
import pandas as pd

def _parse_line(line, lang_code):
    '''
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex
    '''
    ## Dict for language parsing
    lang_dict = {
        'de1': 'St\.',
        'de2': 'Stück',
        'de3': 'St\.',
        'en1': 'pcs',
        'en2': 'pcs',
        'en3': 'pieces',
        'en4': 'pcs',
        'fr': 'pièces',
        'it': 'pz',
        'es': 'piezas',
        'nl1': 'stuks',
        'nl2': 'stuks',
        'cs': 'ks',
        'da': 'stk\.',
        'fi': 'kpl',
        'hr': 'kom',
        'hu': 'db',
        'no': 'stk',
        'pl': 'sztuk',
        'pt': 'unidades',
        'ro': 'buc',
        'sv': 'st',
        'sk': 'ks',
        'sl': 'Število kosov'
    }

    ## Setup regex dict
    rx_dict = {
        "n_pieces": re.compile(rf"(?P<n_pieces>\d+)\s{lang_dict[lang_code]}"),
        "article_num": re.compile(r'(?P<article_num>\d{3}\.\d{3}\.\d{2})')
        }
    
    for key, rx in rx_dict.items():
        match = rx.findall(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def pdf_to_df(uploaded_pdf, lang_code):
    ## Setup pdf layout params
    laparams = LAParams(
        line_overlap=0.1, 
        char_margin=17, 
        line_margin=9, 
        word_margin=0.2, 
        boxes_flow=.1, 
        detect_vertical=False
        )
    
    ## Preparing to read into submission DataFrame
    pdf_dict = {"n_pieces": [], "article_num": []}

    ## Extracting text
    try:
        pdf = extract_text(uploaded_pdf, laparams=laparams)
        for line in pdf.splitlines():
            key, match = _parse_line(line, lang_code=lang_code)
            if match:
                pdf_dict[key].append(match[0])

        ## Check for no-match for language-specific units:
        match_count = 0
        for i in pdf_dict['n_pieces']:
            if i is not None:
                match_count += 1
        # If language specific units are parsed, build df:
        if match_count > 0:
            df = pd.DataFrame(pdf_dict)
            return df
        else:
            return UNABLE_TO_PARSE_LANG
    except:
        return NOT_PDF

def pdf_df_to_dict(df):
    # Strip article dots
    df["article_num"] = df["article_num"].str.replace(".", "", regex=True)
    # Convert n_pieces column to int
    df["n_pieces"] = df["n_pieces"].astype(int)
    return df.set_index('article_num').T.to_dict('index')['n_pieces']

def pdf_df_to_str_list(df):
    pdf_list = []
    for item in df.values.tolist():
        pdf_list.append(f"{item[1]} ({item[0]})")
    return str(pdf_list).replace('[', '').replace("'", '').replace(']', '')
