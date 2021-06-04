import pandas as pd
import re

def form_to_dict(articles_list):
    """
    Transforms form submitted on app to dictionary of article numbers (key) and pieces of each article (value)
    """
    # Setup regex
    rx_dict = {
        'n_pieces': re.compile(r'\((\d*)\)'),
        'article_num': re.compile(r'(\d{8,})')
        }
    real_list = articles_list.replace('.', '').split(', ')

    ## Parsing strings from list
    ## Preparing to read into DataFrame
    df_dict = {'n_pieces': [], 'article_num': []}

    for item in real_list:
        if len(item) >= 9:
            for key, rx in rx_dict.items():
                df_dict[key].append(rx.findall(item)[0])
        else:
            df_dict['n_pieces'].append(1)
            df_dict['article_num'].append(item)

    df = pd.DataFrame(df_dict)

    # Convert n_pieces column to int
    df['n_pieces'] = df['n_pieces'].astype(int)

    df.set_index('article_num').T.to_dict('index')['n_pieces']
