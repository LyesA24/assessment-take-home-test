# Candidate README for Romance Novels take home test.
All of the additional libraries I used have been added to the requirements.txt.

## Task 1
To run process_raw_data.py with command line argument. 'python3.12 process_raw_data.py --path '*filename.csv*'
The output columns have been slightly renamed to preferred names.
The string columns are objects which is the pandas datatype for text. Although I tried to change these specifically to str pandas kept these as objects.


## Task 2
I ran into issues trying to use altair therefore I had to redo this task using matplotlib.

The produced images will be included in the repo however running the code should reproduce
the exact same .png images.

The program can be run normally and requires no inputs.

## Testing
I changed the column names in EXAMPLE_DATA_4.csv to my preferred names but everything else is unchanged.

For test_example_data_4_titles and test_example_data_4_names I am aware tests should only test functions instead of most of the script, however I wanted to verify my script manipulates the data properly.

Run the tests using 'pytest test_analyse_processed_data.py' and 'pytest test_process_raw_data.py'


## Notes
Given more time I would have been able to sort out the clipping between one of the labels
on the bar chart and the boundary box.

I lost .31 on the pylint score for task 2 for unused variables which when removed break the code,
therefore I have left them in.

