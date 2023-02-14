# Homework 03: The World Has Turned and Left Me Turbid
This homework assignment picks up off of our previous assignment. Previously, our robot collected meteorite samples and Mars, taking them back to the Mars lab for analysis. However, in order to analyze these samples, we need clean water. For this assignment we must check the latest water quality data to find out whether it is safe to analyze our samples. 
This assignment lets us practice using JSON, this time not locally, as well as practice unit testing. Our homework 03 directory has two Python scripts: one which holds almost all of our functionality (`analyze_water.py`), and a test script to verify that functionality (`test_analyze_water.py`). 
## Installation
Install the project by cloning the repository as well as downloading Python3 (if not already downloaded). You must also download the `requests` and `pytest` libraries for Python3. This can be done using the following commands in the terminal:
```
$ pip3 install --user requests
...
$ pip3 install --user pytest
```
## Program Descriptions
### Analyze Water
`analyze_water.py`, contains three functions that allow us to do three things: read in a json data file from a url link, calculate turbidity for a given entry from our JSON data, and calculate the required time for the turbidity levels to be below a given threshold. The equations used in our functions for both this script as well as `test_analyze_water.py` come from [here](https://www.fondriest.com/environmental-measurements/measurements/measuring-water-quality/turbidity-sensors-meters-and-methods/). If you would like to access the JSON files we use for the data, it is available on Github [here](https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json). They can be accessed easily using the Python `requests` library as I did.
If executed, this script will prompt the user for an index. The user can put in any number that does not exceed the size of the JSON data file. Once an index is given, the program will calculate the turbidity for that entry's data as well as an average of the next five entries' data. It will also tell us whether the turbidity is above the threshold and how long it will take to lower below the threshold.
### Test Analyze Water
`test_analyze_water.py` is a Python unit test script in order to verify the functionality of the previous `analyze_water.py` script. There is a test for each function in `analyze_water.py`. There could be more tests for this program, but I believe the current tests are sufficient to verify functionality. Further unit testing would be useful mainly for edge cases (e.g. user inputs an index that's out of range). Furthermore, `analyze_water.py` does not have any exception handling. Since there is only one instance of prompting the user, I believe that it is okay if exception handling is not included for now.
## Running the Code
Both of the programs in this directory utilize shebangs, meaning we must create the script executables using the `chmod` command:
```
$ chmod u+x python_script.py
```
After doing so, you can call the Python scripts as standalone executables like so:
```
$ ./python_script.py
```
However, do note that `test_analyze_water.py` is a test script and will not prove very useful when executed via its executable. Instead, for this program we want to use the `pytest` command which will find and automatically run any tests for Python test scripts.
```
$ pytest
```
