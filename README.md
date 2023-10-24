# Spotify Data Visualization

## Pickle a Dictionary
First we need to pickle the data into a dictionary. In pickle_dict.py change the FileDir to match the directory in which the json files are stored. You can also change minSecs as the minimum number of seconds required to keep the entry.
Then, run pickle_dict.py which will create the pickled dictionary. This will be used for plotting.

## Run the Plotting Functions
The plotting functions live in `funcs.py` and are explained within the code. One way to run them is by calling them in `main.py` and then running `python main.py`. As of now, they display the plots without saving. 