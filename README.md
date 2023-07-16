# Spotify Data Visualization

## Pickle a Dictionary
First create a file called `out` which is a dictionary with all of your spotify data.
To do this, go to pickle_dict.py and change the list `StreamingHistoryFileNames` to include your spotify data files. Make sure they are in the directory.
Then, run pickle_dict.py which will create the file `out`. This will be used for plotting.

## Run the Plotting Functions
The plotting functions live in `funcs.py` and are explained within the code. One way to run them is by calling them in `main.py` and then running `python main.py`. As of now, they display the plots without saving. You can view some sample plots in the directory `sample-plots`.