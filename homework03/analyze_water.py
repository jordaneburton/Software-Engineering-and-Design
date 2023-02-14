#!/usr/bin/env python3

import requests # no need to include json library

def get_jsondata( link_to_data ) -> dict:
    """
    This function receives json data from a url. Data will be returned as a 
    Python dictionary
    
    Args:
        link_to_data (str): The url link to the data

    Returns:
        response (dict): The json data; should be formatted into a dictionary
    """
    response = requests.get(url=link_to_data)
    response = response.json()
    return(response)
    
def calculate_turbidity( dict_entry ) -> float:
    """
    This function takes a dictionary entry from our turbidity data and outputs
    the turbidity based on the values in the dictionary. Note this function 
    could be further generalized
    
    Args:
        dict_entry (dict): contains a single dictionary containing AT LEAST
            the keys 'calibration_constant' and 'detector_current'

    Returns:
        turbidity (float): the calculated turbidity value
    """
    a0 = float(dict_entry['calibration_constant']) # Calibration constant
    I90 = float(dict_entry['detector_current']) # Ninety degree detector current
    turbidity = a0 * I90 # Turbidity in NTU Units (0 - 40)
    return(turbidity)

def time_to_return_safe( turb_data, entry_index ) -> int:
    """
    This function calculates the time necessary for turbidity to return to a
    safe threshold. If the turbidity is under threshold, the return value is 0
    If not, it checks each subsequent entry until turbidity is under threshold

    Args:
        turb_data (dict): the dictionary holding our data. MUST HAVE the key 
            'turbidity_data'
        entry_index (int): the index of the dictionary entry holding the desired
            starting data. Entry must be a dictionary that meets requirements set by
            'calculate_turbidity' function
        
    Returns:
        hrs (int): hours til turbidity is under threshold
    """
    DECAY_FACTOR = 0.02 # decay factor per hour, expressed as a decimal
    hrs = 0 # hours elapsed
    T0 = calculate_turbidity(turb_data['turbidity_data'][entry_index]) # Current turbidity
    TURB_THRESHOLD = 1.0 # Turbidity threshold for safe water 
    
    while ( TURB_THRESHOLD < T0*(1-DECAY_FACTOR)**hrs ):
        hrs += 1
        """
        following 2 lines might be unnecessary
        """
        # entry_index += 1
        # T0 = calculate_turbidity(turb_data['turbidity_data'][entry_index])

    return(hrs)
        

def main():
    """
    This function will ask for user to specify an index from the turbidity data
    in order to calculate its turbidity as well as the time needed to return 
    under the turbidity threshold

    No Args or Returns: instead, requests user input
    """
    turbidity_data = get_jsondata('https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')

    data_index = int(input("Enter index of desired data: "))
    turb_avg = 0.0
    
    # Calculate average turbidity of 5 entries starting from 'dict_index'
    for i in range(data_index, data_index + 4):
        current_turb = calculate_turbidity(turbidity_data['turbidity_data'][i])
        turb_avg = turb_avg + current_turb
    turb_avg /= 5
    print("Current turbidity = ", calculate_turbidity(turbidity_data['turbidity_data'][data_index]), "NTU")
    print("Average turbidity based on current and next four measurements = ", turb_avg, " NTU")

    # Calculates time to return to safety threshold
    safe_time = time_to_return_safe(turbidity_data, data_index)
    if ( safe_time > 0 ):
        print("Warning: Turbidity is above threshold for safe use")
    else:
        print("Info: Turbidity is below threshold for safe use")
    print("Minimum time required to return below a safe threshold = ", safe_time, " hours")

if __name__ == '__main__':
    main()
