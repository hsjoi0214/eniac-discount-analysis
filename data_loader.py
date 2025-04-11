""" Import data """

import pandas as pd

def create_valid_path(url):
    return "https://drive.google.com/uc?export=download&id="+url.split("/")[-2]

# products_cl.csv
products_cl = pd.read_csv(
    create_valid_path(
        "https://drive.google.com/file/d/1s7Lai4NSlsYjGEPg1QSOUJobNYVsZBOJ/view?usp=sharing"
        )
    )

# orderlines_cl.csv
orderlines_cl = pd.read_csv(
    create_valid_path(
        "https://drive.google.com/file/d/1lsmAGj5Bt4DZfKbRunyWOyk0fnnV99o8/view?usp=drive_link"
        )
    )

# orders_cl.csv
orders_cl = pd.read_csv(
    create_valid_path(
        "https://drive.google.com/file/d/1jEkjzGsR2PRpeXuDjOY2SY6GlovsuN_L/view?usp=drive_link"
        )
    )

# brands_cl.csv
brands_cl = pd.read_csv(
    create_valid_path(
        "https://drive.google.com/file/d/17L-3ij2yDEgzYVTtHS1fM_ry-bwGq9An/view?usp=drive_link"
        )
    )



