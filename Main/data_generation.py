import time
import pandas as pd


def get_entries(csv_name):
    df = pd.read_csv(f'Main/datasets/{csv_name}_clean.csv')
    items = []
    error_count = 0

    for entry in df.index:
        try:
            processed_entry = [
                df['Product'][entry],
                df['Price Each'][entry],
                df['Order Date'][entry],
            ]
            items.append(processed_entry)
        except:
            error_count += 1
            print(error_count)

    return items

print(get_entries('january'))