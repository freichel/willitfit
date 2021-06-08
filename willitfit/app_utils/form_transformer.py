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
    if (len(articles_list) > 8) and ("," in articles_list):
        real_list = articles_list.split(",")
    elif len(articles_list.strip().replace(".", "")) == 8:
        real_list = [articles_list]
    else:
        raise Exception(LIST_UNREADABLE)
    ## Parsing strings from list
    ## Preparing to read into submission DataFrame
    df_dict = {"n_pieces": [], "article_num": []}

    for item in real_list:
        item_len = len(item.strip())
        if item_len > 10:
            for key, rx in rx_dict.items():
                df_dict[key].append(rx.findall(item)[0])
        else:
            df_dict["n_pieces"].append(1)
            df_dict["article_num"].append(item)

    df = pd.DataFrame(df_dict)
    # Strip article dots
    df["article_num"] = df["article_num"].str.replace(".", "", regex=True)
    # Convert n_pieces column to int
    df["n_pieces"] = df["n_pieces"].astype(int)

    return df.set_index("article_num").T.to_dict("index")["n_pieces"]
