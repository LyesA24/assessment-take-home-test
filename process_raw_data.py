"""A script to process book data."""
# cli accepts 1 argument .csv name.
# Create or overwrite PROCESSED DATA.csv
# collects data from the data file DONE
#The output file should have the following columns only:
#title
#author_name
#year
#rating
#ratings
#"title" and "author_name" should contain text data; all other columns should be numeric.
#In the raw data, many book titles also contain series or format information. To handle this, all titles should be cleaned to remove any information in brackets.
#Any rows with missing values for author or title should not be included in the output.
#The output should be sorted by descending order of rating.
import pandas as pd
import os


def read_csv() -> list[pd.DataFrame]:
    raw_data_dfs = []
    for file in os.listdir('data'):
        if 'AUTHORS' in file:
            author_df = pd.read_csv(f'./data/{file}')
        if 'RAW' in file:
            raw_data_dfs.append(pd.read_csv(f'./data/{file}'))
    raw_df = pd.concat(raw_data_dfs, ignore_index=True)
    return [author_df, raw_df]

def clean_raw_data(raw_book_data: pd.DataFrame) -> pd.DataFrame:
    raw_book_data = raw_book_data.drop(columns=['index', 'Unnamed: 0', 'Unnamed: 0.1'])
    raw_book_data = raw_book_data.dropna()
    return raw_book_data

def left_merge_author_book_data(authors:pd.DataFrame, clean_book_df:pd.DataFrame) -> pd.DataFrame:
    merged_df = clean_book_df.merge(authors, on='author_id', how='left')
    merged_df = merged_df.drop(columns=['author_id'])
    return merged_df
    

if __name__ == "__main__":
    csv_data = read_csv()
    raw_book_data = csv_data[1]
    author_table = csv_data[0]
    clean_book_data = clean_raw_data(raw_book_data)
    merged_df = left_merge_author_book_data(author_table, clean_book_data)
    print(merged_df)
    