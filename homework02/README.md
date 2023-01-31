# Homework 02: No One JSON
The purpose of this project was to practice utilizing JSON to transfer data to and from files. 
In order to do this, we have a scenario in which a robotic vehicle must visit and investigate **five** landing sites on a planet similar in size to Mars.
This directory contains 2 Python scripts (and this README.md); one which randomly generates sites in a specified area of the planet, and another that takes those sites and calculates various statistics for the robot's trip.
## Installation
Install the project by cloning the repository as well as downloading Python3 (if not already downloaded). There is no need to make executables as the Python scripts can be run via the command `python3 py_script.py`.
## Program Descriptions
### Generate Sites
`generate_sites.py`, as the name implies, generates five random sites in a designated area of the planet. The sites will have latitudes between `16.0 - 18.0` degrees North and longitudes between `82.0 - 84.0` degrees East. Once generated, the program will export this data to a JSON file containing a dictionary of a list (of dictionaries).

**Note! `generate_sites.py`, when ran, will create a JSON file named `sites.json`. If you have an existing file of the same name in the same directory as `generate_sites.py`, IT WILL BE OVERWRITTEN when running this program!**

### Calculate Trip
`calculate_trip.py` will take in the data from the generated JSON file, and calculate and print stats for each leg of the robot's trip. Specifically, it will keep track of the current leg (1, 2, etc.), the travel time between each site, and the time required to sample the composition at the current site. After printing these stats for each leg, the program will print out the total number of legs as well as the total time the robot spent on the trip.
## Running the Code
This directory has two programs that must be ran in a certain order: first run `generate_sites.py`, then `calculate_trip.py`. To start, simply type into the terminal:
```
$ python3 generate_sites.py
```
Then type into the terminal:
```
$ python3 calculate_trip.py
```
And the latter program will print out the stats for the robot's randomly generated trip!
