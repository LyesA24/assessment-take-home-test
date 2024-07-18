import pytest
import pandas as pd
from process_raw_data import read_authors_csv, clean_book_df, left_merge_author_book_data, conform_data_to_style, convert_columns_to_single_data_type, sort_data, aesthetic_changes


def test_example_data_4_titles():
    raw_book_tables = pd.read_csv('./data/RAW_DATA_4.csv')
    author_table = read_authors_csv()
    clean_book_table = clean_book_df(raw_book_tables)
    merged_df = left_merge_author_book_data(author_table, clean_book_table)
    conformed_df = conform_data_to_style(merged_df)
    uniform_df = convert_columns_to_single_data_type(conformed_df)
    sorted_df = sort_data(uniform_df)
    pretty_df = aesthetic_changes(sorted_df)
    check_df = pd.read_csv('./data/EXAMPLE_DATA_4.csv')
    assert list(pretty_df['book_title'].values) == list(check_df['book_title'].values)

def test_example_data_4_names():
    raw_book_tables = pd.read_csv('./data/RAW_DATA_4.csv')
    author_table = read_authors_csv()
    clean_book_table = clean_book_df(raw_book_tables)
    merged_df = left_merge_author_book_data(author_table, clean_book_table)
    conformed_df = conform_data_to_style(merged_df)
    uniform_df = convert_columns_to_single_data_type(conformed_df)
    sorted_df = sort_data(uniform_df)
    pretty_df = aesthetic_changes(sorted_df)
    check_df = pd.read_csv('./data/EXAMPLE_DATA_4.csv')
    assert list(pretty_df['author_name'].values) == list(check_df['author_name'].values)

@pytest.fixture
def sample_raw_df():
    return pd.DataFrame({
        'index': [0, 1, 2, 3],
        'Unnamed: 0': [1, 2, 3, 4],
        'Unnamed: 0.1': [1, 2, 3, 4],
        'book_title': ["Book One (Sample Text)", "Book Two (Sample Text)", None, "Book Four (Sample Text)"],
        'Year released': [2019, None, 2017, 2018],
        'ratings': [387, 372, None, 417], 
        'Rating': ['4.0', None, '4.2', '3.8'], 
        'author_id': [1, 2, 3, None]
    })

def test_clean_book_df_columns(sample_raw_df):
    clean_df = clean_book_df(sample_raw_df)
    expected_columns = ['book_title', 'Year released', 'ratings', 'Rating', 'author_id']
    assert list(clean_df.columns) == expected_columns

def test_clean_book_df_drop_rows_with_na(sample_raw_df):
    clean_df = clean_book_df(sample_raw_df)
    assert clean_df.shape[0] == 1 

@pytest.fixture
def sample_df_for_conform_tests():
    return pd.DataFrame({
        'book_title': ["Book One (Sample Text)", "Book Two (Sample Text)"],
        'Rating': ["4.0", "3.8"],
        'ratings': ["387", "372"]
    })

def test_conform_data_to_style_titles(sample_df_for_conform_tests):
    expected_titles = ["Book One", "Book Two"]
    conformed_df = conform_data_to_style(sample_df_for_conform_tests)
    assert list(conformed_df['book_title']) == expected_titles

def test_conform_data_to_style_ratings(sample_df_for_conform_tests):
    expected_ratings = ["4.0", "3.8"]
    conformed_df = conform_data_to_style(sample_df_for_conform_tests)
    assert list(conformed_df['Rating']) == expected_ratings

def test_conform_data_to_style_converted_ratings(sample_df_for_conform_tests):
    expected_converted_ratings = ["387", "372"]
    conformed_df = conform_data_to_style(sample_df_for_conform_tests)
    assert list(conformed_df['ratings']) == expected_converted_ratings

@pytest.fixture
def sample_df_for_conversion():
    return pd.DataFrame({
        'book_title': ["Book One", "Book Two"],
        'name': ["Author One", "Author Two"],
        'Year released': [2019, 2018],
        'ratings': [387, 372],  
        'Rating': [4.0, 3.8] 
    })

def test_convert_columns_to_single_data_type_year_released(sample_df_for_conversion):
    converted_df = convert_columns_to_single_data_type(sample_df_for_conversion)
    assert converted_df['Year released'].dtype == int

def test_convert_columns_to_single_data_type_ratings(sample_df_for_conversion):
    converted_df = convert_columns_to_single_data_type(sample_df_for_conversion)
    assert converted_df['ratings'].dtype == int

def test_convert_columns_to_single_data_type_rating(sample_df_for_conversion):
    converted_df = convert_columns_to_single_data_type(sample_df_for_conversion)
    assert converted_df['Rating'].dtype == float

@pytest.fixture
def sample_df_for_sorting():
    return pd.DataFrame({
        'book_title': ["Book One", "Book Two", "Book Three"],
        'Rating': [3.8, 4.0, 3.7]
    })

def test_sort_data_order(sample_df_for_sorting):
    sorted_df = sort_data(sample_df_for_sorting)
    expected_order = ["Book Two", "Book One", "Book Three"]
    assert list(sorted_df['book_title']) == expected_order

def test_sort_data_shape(sample_df_for_sorting):
    sorted_df = sort_data(sample_df_for_sorting)
    expected_shape = (3, 2)
    assert sorted_df.shape == expected_shape

@pytest.fixture
def sample_authors_df():
    return pd.DataFrame({
        'author_id': [1, 2, 3, 4],
        'author_name': ['Author One', 'Author Two', 'Author Three', 'Author Four']
    })

@pytest.fixture
def sample_clean_df_for_merge():
    return pd.DataFrame({
        'book_title': ["Book One (Sample Text)", "Book Two (Sample Text)", "Book Three (Sample Text)", "Book Four (Sample Text)"],
        'Year released': [2019, 2018, 2017, 2016],
        'ratings': [387, 372, 417, 450],
        'Rating': ['4.0', '3.8', '4.2', '4.5'],
        'author_id': [1, 2, 3, 4]
    })

def test_left_merge_author_book_data_columns(sample_authors_df, sample_clean_df_for_merge):
    
    merged_df = left_merge_author_book_data(sample_authors_df, sample_clean_df_for_merge)
    expected_columns = ['book_title', 'Year released', 'ratings', 'Rating', 'author_name']
    assert list(merged_df.columns) == expected_columns

def test_left_merge_author_book_data_shape(sample_authors_df, sample_clean_df_for_merge):
    merged_df = left_merge_author_book_data(sample_authors_df, sample_clean_df_for_merge)
    expected_shape = (4, 5)  
    assert merged_df.shape == expected_shape


