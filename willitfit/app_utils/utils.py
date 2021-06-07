import pandas as pd
import os
from willitfit.params import CAR_DATABASE, PROJECT_DIR, PROJECT_NAME, DATA_FOLDER
from pathlib import Path
import os

def get_car_data():
    """
    Read CSV into DataFrame
    """
    data = pd.read_csv(
        PROJECT_DIR/PROJECT_NAME/DATA_FOLDER/CAR_DATABASE
        )
    
    return data

def gen_make_list(data):
    """
    Generate frontend list of car makes
    """
    ## Generate Make and Model lists for Front-end
    make_list = data['make'].value_counts().index.to_list()
    return sorted(make_list)

def gen_make_dict(data):
    """
    Generate make dictionary with list of models as values for frontend use
    """
    make_list = gen_make_list(data)
    ## Lower snake naming convention
    make_list_lower_snake = [i.lower().replace(' ', '_') for i in make_list]
    ## Group by make
    by_make = data.groupby('make')
    for i, make in enumerate(make_list_lower_snake):
        vars()[f"{make}_df"] = by_make.get_group(make_list[i])
    ## Generate list of lists for zipping into dict
    by_make_list = []
    for make in make_list_lower_snake:
        vars()[f"{make}_list"] = sorted(vars()[f"{make}_df"]['car_model'].to_list())
        by_make_list.append(vars()[f"{make}_list"])
        
    MAKE_DICT = dict(zip(make_list, by_make_list))
    return MAKE_DICT


if __name__ == "__main__":
    print(get_car_data())