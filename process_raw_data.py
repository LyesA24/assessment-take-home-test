"""Transform script reads raw csv data and outputs PROCESSED_DATA.csv"""
import os
import argparse
import pandas as pd

DEFAULT_FILENAME = 'PROCESSED_DATA.csv'

type_conversion_dict = {
    'book_title': str,
    'name': str,
    'Year released': int,
    'ratings': int,
    'Rating': float
}

column_rename_dict = {
    'Year released': 'year_released' ,
    'ratings': 'ratings_count',
    'Rating': 'rating',
    'name': 'author_name' 
}

column_order = ['book_title', 'author_name', 'year_released', 'rating', 'ratings_count']

def get_parser_arguments() -> str:
    """Adds command line functionality for the output file path."""
    parser = argparse.ArgumentParser(description="""Transform raw books data and author data,
                                     and output processed_data.csv .""")
    parser.add_argument('--path', nargs='?', type=str, default=DEFAULT_FILENAME,
                        help="Choose a file path, default is 'PROCESSED_DATA.csv'")
    args = parser.parse_args()
    path =args.path
    # Validation for empty string input:
    if not path:
        raise ValueError("""'--path' present but no string input.
                        --path argument must be in format '--path filename.csv'""")
    # Validation check for singular .csv in string:
    if path.count('.csv') == 1:
        return path
    raise ValueError("""--path must be in format '--path filename.csv'.""")

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

def merge_book_dfs(book_df_list: list[pd.DataFrame]) -> pd.DataFrame:
    """Combines the separate book DataFrame tables."""
    return pd.concat(book_df_list, ignore_index=True)

def clean_book_df(raw_book_df: pd.DataFrame) -> pd.DataFrame:
    """Drops unused columns and rows containing na values from DataFrame"""
    raw_book_df = raw_book_df.drop(columns=['index', 'Unnamed: 0', 'Unnamed: 0.1'])
    raw_book_df = raw_book_df.dropna()
    return raw_book_df

def left_merge_author_book_data(authors: pd.DataFrame, clean_book_df:pd.DataFrame) -> pd.DataFrame:
    """Left joins book data table to authors data table."""
    df = clean_book_df.merge(authors, on='author_id', how='left')
    df = df.drop(columns=['author_id'])
    return df

def conform_data_to_style(unconformed_df: pd.DataFrame) -> pd.DataFrame:
    """
    Conforms data to remove unwanted characters
    or information in brackets.
    """
    unconformed_df['book_title'] = (unconformed_df['book_title'].str.replace
                                    (r'\s*\([^)]*\)', '', regex=True))
    unconformed_df['Rating'] = unconformed_df['Rating'].str.replace(',', '.')
    unconformed_df['ratings'] = unconformed_df['ratings'].str.replace("'", '').str.replace("`", '')
    return unconformed_df


def convert_columns_to_single_data_type(incorrect_types_df: pd.DataFrame) -> pd.DataFrame:
    """Converts columns to single data types."""
    return incorrect_types_df.astype(type_conversion_dict)

def sort_data(unsorted_df: pd.DataFrame) -> pd.DataFrame:
    """Orders book rows by rating value"""
    return unsorted_df.sort_values(by='Rating', ascending=False)

def export_to_csv(final_df: pd.DataFrame, filepath) -> pd.DataFrame:
    """Exports the file to csv"""
    final_df.to_csv(filepath, index=False)

def aesthetic_changes(ugly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Improves the look of the columns by changing the names to a uniform style,
    and reordering the columns into a more coherent order.
    """
    ugly_df = ugly_df.rename(columns=column_rename_dict)
    return ugly_df[column_order]



if __name__ == "__main__":
    filename = get_parser_arguments()
    raw_book_tables = read_raw_data_csvs()
    author_table = read_authors_csv()
    concatenated_book_table = merge_book_dfs(raw_book_tables)
    clean_book_table = clean_book_df(concatenated_book_table)
    merged_table = left_merge_author_book_data(author_table, clean_book_table)
    conformed_table = conform_data_to_style(merged_table)
    uniform_table = convert_columns_to_single_data_type(conformed_table)
    sorted_table = sort_data(uniform_table)
    pretty_table = aesthetic_changes(sorted_table)
    export_to_csv(pretty_table, filename)
