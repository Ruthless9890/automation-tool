# functions for setting up the webdriver, handling errors, or managing csv files

import pandas as pd

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)