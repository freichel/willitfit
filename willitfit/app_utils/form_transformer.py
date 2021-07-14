import pandas as pd
import re
from willitfit.params import LIST_UNREADABLE


def form_to_dict(articles_list):
    """
    Transform form submitted on app to dataframe
    """
    ## Setup regex
    rx_dict = {
    "n_pieces": re.compile(r'\((\d+)\)'),
    "article_num": re.compile(r'(\d{3}\.*\d{3}\.*\d{2})')
    }
    ## Split Form string delimited by comma to list
    # Error check
    input_val_bool = (articles_list.replace('.', '').replace('(', '').replace(')', '').replace(',', '').replace(' ', '').isnumeric())\
        and (len(articles_list.replace(' ','').strip(',').replace('.', '')) >= 8)

    if input_val_bool:
        real_list = articles_list.replace('.', '').replace(' ', '').strip(',').split(',')
        ## Parsing strings from list
        ## Empty dict for dataframe prep
        df_dict = {"n_pieces": [], "article_num": []}
        ## Errors counter
        errors = 0
        for item in real_list:
            ## Check if article_num before bracket satisfies the right number of integers
            if (len(item.split('(')[0]) == 8) and (len(item) >= 11):
                for key, rx in rx_dict.items():
                    df_dict[key].append(rx.findall(item)[0])
            elif len(item) == 8:
                df_dict["n_pieces"].append(1)
                df_dict["article_num"].append(item)
            else:
                errors += 1
        if errors == 0:
            df = pd.DataFrame(df_dict)
            # Strip article dots
            df["article_num"] = df["article_num"].str.replace(".", "", regex=True)
            # Convert n_pieces column to int
            df["n_pieces"] = df["n_pieces"].astype(int)
            return df.set_index("article_num").T.to_dict("index")["n_pieces"]
    return LIST_UNREADABLE
