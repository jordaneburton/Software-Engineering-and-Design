import random
import math
import json

mars_radius = 3389.5    # km
robot_speed = 10    # km per hr

### functions to be used in the code

def calc_gcd(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:    # function from Slack that calculates great circle distance
    lat1, lon1, lat2, lon2 = map( math.radians, [latitude_1, longitude_1, latitude_2, longitude_2] )
    d_sigma = math.acos( math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(abs(lon1-lon2)))
    return ( mars_radius * d_sigma )

def calc_traveltime(distance: float) -> float:  # function for calculating travel time from one site to another
    return distance/robot_speed

def get_sampletime(sample: str) -> float:  # function to sort samples for time
    if (sample == "stony"):
        return 1. # hour 
    elif (sample == "iron"):
        return 2. 
    elif (sample == "stony-iron"):
        return 3.

def calc_trip(site_dict): # main function that calculates various stats for the trip
    trip_time = 0.  # trip stats
    trip_legs = 0

    leg_id = 0      # leg stats
    leg_dist = 0.
    leg_time = 0.
    sample_time = 0.

    startlat = 16.0     # starting position for robot
    startlong = 82.0
    endlat = 0.
    endlong = 0.
    for i in range(len(site_dict['sites'])): # use previous functions to produce stats for each leg
        endlat = site_dict['sites'][i]['latitude']
        endlong = site_dict['sites'][i]['longitude']
        leg_id = site_dict['sites'][i]['site_id']
        
        leg_dist = calc_gcd(startlat, startlong, endlat, endlong)   # calculate travel distance in leg
        leg_time = calc_traveltime(leg_dist)    # calculate travel time for current leg
        sample_time = get_sampletime(site_dict['sites'][i]['composition'])  # get sample time
        trip_legs += 1
        trip_time += leg_time + sample_time

        print('leg = ', leg_id, ', time to travel = ', round(leg_time,3), ' hr, time to sample = ', round(sample_time,3), ' hr')  # print stats for current leg

        startlat = site_dict['sites'][i]['latitude']    # set new starting point for robot
        startlong = site_dict['sites'][i]['longitude']
    return [trip_legs, trip_time]


### main part of program that runs when executed

with open('sites.json', 'r') as f:
    site_data = json.load(f)

[num_of_legs, total_time] = calc_trip(site_data)
print('============================')
print('number of legs = ', round(num_of_legs,3), ', total time elapsed = ', round(total_time,3), ' hr')
