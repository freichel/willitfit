import pandas as pd
import re

def form_to_dict(articles_list):
    """
    Transform form submitted on app to dataframe 
    """
    ## Setup regex
    rx_dict = {
    'n_pieces': re.compile(r'\((\d+)\)'),
    'article_num': re.compile(r'(\d{3}\.\d{3}\.\d{2,})')
    }
    ## Split Form string delimited by comma to list
    real_list = articles_list.split(', ')


    ## Parsing strings from list
    ## Preparing to read into submission DataFrame
    df_dict = {'n_pieces': [], 'article_num': []}

    for item in real_list:
        if len(item) > 10:
            for key, rx in rx_dict.items():
                df_dict[key].append(rx.findall(item)[0])
        else:
            df_dict['n_pieces'].append(1)
            df_dict['article_num'].append(item)

    df = pd.DataFrame(df_dict)
    # Strip article dots
    df['article_num'] = df['article_num'].str.replace('.', '')
    # Convert n_pieces column to int
    df['n_pieces'] = df['n_pieces'].astype(int)
    # Transform back to key, list pairs
    return df.set_index('article_num').T.to_dict('list')
