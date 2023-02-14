#!/usr/bin/env python3

from analyze_water import get_jsondata, calculate_turbidity, time_to_return_safe
import pytest

def test_get_jsondata():
    assert type(get_jsondata("https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json")) == dict

inner_dict = {
        'calibration_constant': 1,
        'detector_current': 1
        }
test_dict = { 'turbidity_data': inner_dict }

def test_calculate_turbidity():
    with pytest.raises(KeyError):
        calculate_turbidity(test_dict)

def test_time_to_return_safe():
    with pytest.raises(KeyError):
        time_to_return_safe(test_dict, 0)

