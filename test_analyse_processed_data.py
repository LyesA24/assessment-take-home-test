import pytest
import pandas as pd
from analyse_processed_data import prepare_decades_releases_data, prepare_top_authors_data, create_pie_chart_labels

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'book_title': ["Book One", "Book Two", "Book Three", "Book Four"],
        'year_released': [1985, 1995, 2005, 2015],
        'ratings_count': [500000, 1000000, 1500000, 2000000],
        'author_name': ["Author A", "Author B", "Author C", "Author A"]
    })

def test_prepare_decades_releases_data_columns(sample_data):
    result_df = prepare_decades_releases_data(sample_data)
    expected_columns = ['decade', 'count']
    assert list(result_df.columns) == expected_columns

def test_prepare_decades_releases_data_shape(sample_data):
    result_df = prepare_decades_releases_data(sample_data)
    expected_shape = (4, 2)
    assert result_df.shape == expected_shape

def test_prepare_decades_releases_data_values(sample_data):
    result_df = prepare_decades_releases_data(sample_data)
    expected_values = {
        'decade': [1980, 1990, 2000, 2010],
        'count': [1, 1, 1, 1]
    }
    for column, expected in expected_values.items():
        assert list(result_df[column]) == expected

def test_prepare_top_authors_data_columns(sample_data):
    result_df = prepare_top_authors_data(sample_data)
    expected_columns = ['author_name', 'ratings_count']
    assert list(result_df.columns) == expected_columns

def test_prepare_top_authors_data_shape(sample_data):
    result_df = prepare_top_authors_data(sample_data)
    expected_shape = (3, 2)
    assert result_df.shape == expected_shape

def test_prepare_top_authors_data_values(sample_data):
    result_df = prepare_top_authors_data(sample_data)
    expected_values = {
        'author_name': ["Author A", "Author C", "Author B"],
        'ratings_count': [2500000, 1500000, 1000000]
    }
    for column, expected in expected_values.items():
        assert list(result_df[column]) == expected


def test_create_pie_chart_labels_values():
    sample_data = pd.DataFrame({
        'decade': [1980, 1990, 2000, 2010],
        'count': [1, 1, 1, 1]
    })
    result_labels = create_pie_chart_labels(sample_data)
    expected_labels = [
        '1980s: 1 (25.0%)',
        '1990s: 1 (25.0%)',
        '2000s: 1 (25.0%)',
        '2010s: 1 (25.0%)'
    ]
    assert result_labels == expected_labels