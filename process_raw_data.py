"""A script to process book data."""
import os
import pandas as pd


type_conversion_dict = {
    'book_title': str,
    'name': str,
    'Year released': int,
    'ratings': int,
    'Rating': float
}

def read_raw_data_csvs() -> list[pd.DataFrame]:
    """Reads data from RAW_DATA csv files and returns a list of
     DataFrames for each CSV """
    raw_book_dfs = []
    for file in os.listdir('data'):
        if 'RAW' in file:
            raw_book_dfs.append(pd.read_csv(f'./data/{file}'))
    return raw_book_dfs

def read_authors_csv() -> pd.DataFrame:
    """Reads data from authors csv and returns authors DataFrame"""
    for file in os.listdir('data'):
        if 'AUTHORS' in file:
            return pd.read_csv(f'./data/{file}')
        return None

def merge_book_dfs(book_df_list:list[pd.DataFrame]) -> pd.DataFrame:
    """Combines the separate book DataFrame tables."""
    return pd.concat(book_df_list, ignore_index=True)

def remove_na_from_book_df(raw_book_df: pd.DataFrame) -> pd.DataFrame:
    """Drops unused columns and rows containing na values from DataFrame"""
    raw_book_df = raw_book_df.drop(columns=['index', 'Unnamed: 0', 'Unnamed: 0.1'])
    raw_book_df = raw_book_df.dropna()
    return raw_book_df

def left_merge_author_book_data(authors:pd.DataFrame, clean_book_df:pd.DataFrame) -> pd.DataFrame:
    """Left joins book data table to authors data table."""
    df = clean_book_df.merge(authors, on='author_id', how='left')
    df = df.drop(columns=['author_id'])
    return df

def conform_data_to_style(unconformed_df:pd.DataFrame) -> pd.DataFrame:
    """Conforms data to remove unwanted characters
    or information in brackets."""
    unconformed_df['book_title'] = (unconformed_df['book_title'].str.replace
                                    (r'\s*\([^)]*\)', '', regex=True))
    unconformed_df['Rating'] = unconformed_df['Rating'].str.replace(',', '.')
    unconformed_df['ratings'] = unconformed_df['ratings'].str.replace("'", '').str.replace("`", '')
    return unconformed_df


def convert_columns_to_single_data_type(incorrect_types_df:pd.DataFrame) -> pd.DataFrame:
    """Converts columns to single data types."""
    return incorrect_types_df.astype(type_conversion_dict)

def sort_data(unsorted_df:pd.DataFrame) -> pd.DataFrame:
    """Orders book rows by rating value"""
    return unsorted_df.sort_values(by='Rating', ascending=False)

def export_to_csv(final_df:pd.DataFrame, filename) -> pd.DataFrame:
    """Exports the file to csv"""
    final_df.to_csv(filename, index=False)


if __name__ == "__main__":
    raw_book_tables = read_raw_data_csvs()
    author_table = read_authors_csv()
    concatenated_book_df = merge_book_dfs(raw_book_tables)
    clean_book_table = remove_na_from_book_df(concatenated_book_df)
    merged_df = left_merge_author_book_data(author_table, clean_book_table)
    conformed_df = conform_data_to_style(merged_df)
    uniform_df = convert_columns_to_single_data_type(conformed_df)
    sorted_df = sort_data(uniform_df)
    export_to_csv(sorted_df, 'PROCESSED_DATA.csv')
