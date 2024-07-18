"""A script that reads processed book data, and creates
a pie chart and bar chart."""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

FILENAME = 'PROCESSED_DATA.csv'
PIE_CHART_FILENAME = 'decade_releases.png'
BAR_CHART_FILENAME = 'top_authors.png'

def read_processed_data_csv()->pd.DataFrame:
    """Reads processed data CSV"""
    return pd.read_csv(FILENAME)

def prepare_decades_releases_data(raw_data:pd.DataFrame)->pd.DataFrame:
    """
    Takes data loaded from CSV and return a table for decades
    and number of total books.
    """
    raw_data['decade'] = (raw_data['year_released'] // 10) * 10
    return raw_data.groupby('decade').size().reset_index(name='count')

def prepare_top_authors_data(raw_data:pd.DataFrame)->pd.DataFrame:
    """
    Takes data loaded from CSV, and returns a table for the
    total number of ratings for the ten most-rated authors.
    """
    author_ratings = raw_data.groupby('author_name')['ratings_count'].sum().reset_index()
    return author_ratings.sort_values(by='ratings_count', ascending=False).head(10)

def create_pie_chart_labels(decade_releases_df:pd.DataFrame)->pd.DataFrame:
    """Creates the labels for the pie chart legend"""
    labels = decade_releases_df['decade'].astype(str) + 's'
    sizes = decade_releases_df['count']
    total = sizes.sum()
    return [f'{label}: {count} ({count/total:.1%})' for label, count in zip(labels, sizes)]


def create_pie_chart(decade_releases_df:pd.DataFrame)->None:
    """
    Creates a pie chart showing the proportion of books 
    released in each decade. Exports it as a png image.
    """
    legend_labels = create_pie_chart_labels(decade_releases_df)
    # Set color map and retrieve color for each decade:
    cmap = plt.get_cmap("tab20")
    colors = cmap(np.linspace(0, 1, len(decade_releases_df['count'])))
    # Set chart size:
    plt.figure(figsize=(10, 8))
    patches, texts = plt.pie(decade_releases_df['count'], startangle=140, colors=colors)
    # Create legend and anchor it outside of the chart:
    plt.legend(patches, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))
    plt.title('Proportion of Books Released per Decade')
    plt.axis('equal')
    # Save chart:
    plt.savefig(PIE_CHART_FILENAME, bbox_inches='tight')
    plt.close()

def millions(x, pos):
    """Used to format x-axis labels"""
    return '%1.1fM' % (x * 1e-6)


def create_bar_chart(top_authors_data:pd.DataFrame)->None:
    """
    Creates a sorted bar chart showing the total number of
    ratings for the ten most-rated authors. Exports it as a png image.
    """
    # Set chart size:
    plt.figure(figsize=(14, 10))
    bars = plt.barh(top_authors_data['author_name'],
                     top_authors_data['ratings_count'], color='blue')
    plt.xlabel('Total Number of Ratings')
    plt.ylabel('Author')
    plt.title('Top 10 Most-Rated Authors')
    plt.gca().invert_yaxis()
    # Formatting x-axis labels:
    formatter = FuncFormatter(millions)
    plt.gca().xaxis.set_major_formatter(formatter)
    # Adding label to each bar:
    for a_bar in bars:
        width = a_bar.get_width()
        label_x_pos = width + (max(top_authors_data['ratings_count'])
                               * 0.01)
        plt.text(label_x_pos, a_bar.get_y() + a_bar.get_height()/2, f'{width:,.0f}', va='center')
    # Save chart:
    plt.savefig(BAR_CHART_FILENAME, bbox_inches='tight')
    plt.close()



if __name__ == "__main__":
    csv_data_df = read_processed_data_csv()
    pie_chart_data = prepare_decades_releases_data(csv_data_df)
    bar_chart_data = prepare_top_authors_data(csv_data_df)
    create_pie_chart(pie_chart_data)
    create_bar_chart(bar_chart_data)
