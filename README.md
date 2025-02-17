# Take Home Task - Romance Novels

You've been hired as a contractor by Adora Enhance, a company that focuses on book marketing in the romance sector. They've asked you to work on developing a data pipeline they use to understand what titles are popular in the genre.

Adora Enhance currently makes use of a web scraping tool to extract data regularly from their sales platform, but this produces a messy and error-filled output. They'd like you to develop the `transform` stage of the pipeline, building a repeatable process that allows them to clean data for analysis.

You have two specific tasks to complete:

1. Build a transform script that takes the initial raw scraped data and produces a clean, consistent result
2. Build an analysis script that takes the processed data and produces simple visualisations from it

## Resources

A number of resources are required for this project; these are provided in `data.zip`:

- `AUTHORS.csv`: a dataset of author names and IDs
- `RAW_DATA_0.csv`: an example file for processing
- `RAW_DATA_1.csv`: a second example file
- `RAW_DATA_4.csv`: a third example file
- `EXAMPLE_PROCESSED_4.csv`: an example of a processed file made using `RAW_DATA_4.csv`

## Assessment

There are no automated tests to guide you on this assessment. Instead, your code will be holistically assessed on two aspects:

- How well does it work?
- How well is it written?

During this assessment, you should focus on ensuring that you write high-quality, organised code that meets the requirements of the tasks.

## Task 1

Create a Python script - `process_raw_data.py`. This script should run from the command line and accept one argument: the path to a `.csv` file.

When run, the script should process a file in the same format as `RAW_DATA_0.csv`, `RAW_DATA_1.CSV`, and `RAW_DATA_4.csv`. It should produce a single `.csv` file as output named `PROCESSED_DATA.csv`. This file should match the format of `EXAMPLE_PROCESSED_4.csv`.

Any previous `PROCESSED_DATA.csv` file should be overwritten entirely, with the new file only containing data from the current raw data file.

The output file should have the following columns only:

- title
- author_name
- year 
- rating
- ratings

"title" and "author_name" should contain text data; all other columns should be numeric.

In the raw data, many book titles also contain series or format information. To handle this, all titles should be cleaned to remove any information in brackets.

Any rows with missing values for author or title should not be included in the output.

The output should be sorted by descending order of rating.

## Task 2

Create a second Python script - `analyse_processed_data.py`.

When run, this script should load a `PROCESSED_DATA.csv` file and produce the following file outputs:

- `decade_releases.png`: a pie chart showing the proportion of books released in each decade.
- `top_authors.png`: a sorted bar chart showing the total number of ratings for the ten most-rated authors.
