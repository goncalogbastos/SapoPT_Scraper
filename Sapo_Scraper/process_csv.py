import os
import pandas as pd

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


df_list = []

for filename in os.listdir('scraped_data'):
    my_file = os.path.join(THIS_FOLDER, 'scraped_data')
    my_file = os.path.join(my_file, filename)
    df_list.append(pd.read_csv(my_file))

merged_df = pd.concat(df_list, axis=0, ignore_index=True)