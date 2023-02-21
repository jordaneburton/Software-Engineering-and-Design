# Homework 04: Buddy Flask
In this homework assignment, we have found an abundance of interesting positional and velocity data for the International Space Station (ISS). Our objective is to build a Flask application for querying and returning the positional and translational information from the ISS data set.
This assignment lets us practice using Flask to run a local development server while implementing various "routes" or API endpoints in a Flask Python program. Our homework 04 directory contains a single Python script built to run a local Flask server(`iss_tracker.py`). Once this program is running, we can make queries using curl in order to access our various routes and information.
## Installation
Install the project by cloning the repository. You must also download the `requests`,`flask`, and `xmltodict` libraries for Python3. This can be done using the following commands in the terminal (replace "library" with the desired Python library):
```
$ pip3 install --user library
```
## Program Description
### ISS Tracker
`iss_tracker.py`, contains four routes that allow us to query various information about the ISS. The data that we are querying is the "Orbital Ephemeris Message" data from the [ISS Trajectory Data](https://spotthestation.nasa.gov/trajectory_data.cfm) website. If you would like to access the XML files we use for the data, it is available [here](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml). They can be accessed easily using the Python `requests` library as I did.
When executed, this program will begin to run a Flask development server on the current terminal window. You will need to open a separate window in order to make queries.
### Routes and Queries
In our program, we have four routes you can use to query information (replace "\<epoch\>" with the entry, e.g. 0, 1, ... etc.):
| **Route** | **Info Returned** |
|---|---|
| `/` | A list of all the data from the set (all Epochs and their positions and velocities) |
| `/epoch` | A list of just the Epochs in the dataset |
| `/epoch/<epoch>` | State vectors for a specific Epoch in the dataset |
| `/epoch/<epoch>/speed` | Instantaneous speed for a specific Epoch |
## Running the Code
In order to properly run this program, you will need to open two terminal windows. One window will be used to run the Flask server, while the other will be used to make queries. Start by running the Flask Python program in the first window via the following command (make sure to exclude .py from the end of the program name):
```
$ flask --app iss_tracker --debug run
 * Serving Flask app 'iss_tracker'
 * Debug mode: on
...
...

 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 338-365-775
```
After doing so, open the second terminal window and try to make a query using the following route:
```
$ curl localhost:5000/
```
This route returns ALL of the data from the set (which is a lot) so most likely you won't see the beginning of the data, but after that command, your window should look similar to this:
```
...
...

  [
    "2023-063T11:59:00.000Z",
    "X = 2511.5681106492402km",
    "Y = -5991.3267501460596km",
    "Z = 1991.1683453687999km",
    "X_DOT = 5.2410359153923798km/s",
    "Y_DOT = 0.32894397165270001km/s",
    "Z_DOT = -5.57976406061041km/s"
  ],
  [
    "2023-063T12:00:00.000Z",
    "X = 2820.04422055639km",
    "Y = -5957.89709645725km",
    "Z = 1652.0698653803699km",
    "X_DOT = 5.0375825820999403km/s",
    "Y_DOT = 0.78494316057540003km/s",
    "Z_DOT = -5.7191913150960803km/s"
  ]
]
$
```

Here are some more examples of what your results should look like when you use the other three routes:
This is an example for `/epoch`
```
$ curl localhost:5000/epoch
...
...

... '2023-063T11:27:00.000Z', '2023-063T11:31:00.000Z', '2023-063T11:35:00.000Z', '2023-063T11:39:00.000Z', '2023-063T11:43:00.000Z', '2023-063T11:47:00.000Z', '2023-063T11:51:00.000Z', '2023-063T11:55:00.000Z', '2023-063T11:59:00.000Z', '2023-063T12:00:00.000Z']
$
```

This is an example for `/epoch/<epoch>`
```
$ curl localhost:5000/epoch/0
EPOCH entry 0: 2023-048T12:00:00.000Z
$
```

This is an example for `/epoch/<epoch>/speed`
```
$ curl localhost:5000/epoch/0/speed
EPOCH entry 0: 2023-048T12:00:00.000Z
Calculated speed to be: 7.658223206788738 km/s
$
```
