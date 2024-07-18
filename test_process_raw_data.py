import pandas as pd
from process_raw_data import read_authors_csv, merge_book_dfs, remove_na_from_book_df, left_merge_author_book_data, conform_data_to_style,convert_columns_to_single_data_type, sort_data, aesthetic_changes

def test_example_passes():
    raw_book_tables = pd.read_csv('./data/RAW_DATA_4.csv')
    author_table = read_authors_csv()
    clean_book_table = remove_na_from_book_df(raw_book_tables)
    merged_df = left_merge_author_book_data(author_table, clean_book_table)
    conformed_df = conform_data_to_style(merged_df)
    uniform_df = convert_columns_to_single_data_type(conformed_df)
    sorted_df = sort_data(uniform_df)
    pretty_df = aesthetic_changes(sorted_df)
    check_df = pd.read_csv('./data/EXAMPLE_DATA_4.csv')
    assert pretty_df == check_df
    