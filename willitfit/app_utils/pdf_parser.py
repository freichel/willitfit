from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import re
import pandas as pd
from willitfit.app_utils.utils import _parse_line
from willitfit.params import IKEA_WEBSITE_LANGUAGE

def pdf_to_dict(uploaded_pdf, IKEA_WEBSITE_LANGUAGE):
    ## Setup pdf layout params
    laparams = LAParams(
        line_overlap=0.1, 
        char_margin=17, 
        line_margin=9, 
        word_margin=0.2, 
        boxes_flow=.1, 
        detect_vertical=False
        )
    ## Extracting text
    pdf = extract_text(uploaded_pdf, laparams=laparams)
    
    ## Dict for language parsing
    lang_dict = {
        'de': 'St\.',
        'en': 'pcs',
        'fr': 'pièces',
        'it': 'pz',
        'es': 'piezas',
        'nl': 'stuks',
        'cs': 'ks',
        'da': 'stk\.',
        'fi': 'kpl',
        'hr': 'kom',
        'hu': 'db',
        'no': 'stk',
        'pl': 'sztuk',
        'pt': 'unidades',
        'ro': 'buc',
        'se': 'st',
        'sk': 'ks',
        'sl': 'Število kosov'
    }

    ## Setup regex dict
    rx_dict = {
        'n_pieces': re.compile(rf"(?P<n_pieces>\d+)\s{lang_dict[IKEA_WEBSITE_LANGUAGE]}"),
        'article_num': re.compile(r'(?P<article_num>\d{3}\.\d{3}\.\d{2,})')
        }

    ## Preparing to read into submission DataFrame
    pdf_dict = {'n_pieces': [], 'article_num': []}

    for line in pdf.splitlines():
        key, match = _parse_line(line)
        if match:
            pdf_dict[key].append(match[0])

    df = pd.DataFrame(pdf_dict)
    # Strip article dots

    df['article_num'] = df['article_num'].str.replace('.', '', regex=True)
    # Convert n_pieces column to int
    df['n_pieces'] = df['n_pieces'].astype(int)

    return df.set_index('article_num').T.to_dict('index')['n_pieces']

