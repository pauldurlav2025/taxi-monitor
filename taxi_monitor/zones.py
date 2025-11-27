import random
import numpy
from matplotlib.path import Path

class TaxiZone:
    def __init__(
        self,  
        coordinates
    ):
        numpy.array(coordinates)
        self.zone_polygon = Path(coordinates)

# TODO: Replace with actual taxi zone coordinates
TAXI_ZONES = {
    "Kolkata": TaxiZone([
        [40.71, -74.02], 
        [40.72, -74.01], 
        [40.73, -73.99], 
        [40.71, -73.98]
    ]),
    "Kalyani": TaxiZone([
        [40.63, -73.78], 
        [40.65, -73.79], 
        [40.66, -73.76], 
        [40.64, -73.74]
    ]),
    "Barrackpore": TaxiZone([
        [40.80, -74.00], 
        [40.82, -74.01], 
        [40.83, -73.98], 
        [40.81, -73.97]
    ]),
    "Bardhmann": TaxiZone([
        [40.85, -73.92], 
        [40.87, -73.93], 
        [40.88, -73.89], 
        [40.86, -73.88]
    ]),
    "Asansol": TaxiZone([
        [40.76, -73.97], 
        [40.78, -73.98], 
        [40.79, -73.96], 
        [40.77, -73.95]
    ]),
    "Siliguri": TaxiZone([
        [40.70, -74.01], 
        [40.71, -74.00], 
        [40.70, -73.99], 
        [40.69, -74.00]
    ]),
    "Darjeeling": TaxiZone([
        [40.69, -73.99], 
        [40.70, -73.97], 
        [40.68, -73.96], 
        [40.67, -73.98]
    ]),
    "Basirhat": TaxiZone([
        [40.75, -73.94], 
        [40.76, -73.92], 
        [40.74, -73.91], 
        [40.73, -73.93]
    ]),
    "Purulia": TaxiZone([
        [40.78, -73.96], 
        [40.79, -73.95], 
        [40.80, -73.93], 
        [40.79, -73.92]
    ]),
    "Mednipur": TaxiZone([
        [40.75, -73.99], 
        [40.76, -73.98], 
        [40.77, -73.97], 
        [40.76, -73.96]
    ])
}


def get_current_zone(
    taxi_latitude, 
    taxi_longitude
):
    for zone_name in TAXI_ZONES:
        if TAXI_ZONES[zone_name].zone_polygon.contains_point((
            taxi_latitude, 
            taxi_longitude
        )):
            return zone_name
            
    return "OUTSIDE_TAXI_ZONES"

def get_random_start_location() -> tuple:
    center_lat = 40.75
    center_lon = -73.98
    
    start_lat = center_lat + random.uniform(-0.005, 0.005)
    start_lon = center_lon + random.uniform(-0.005, 0.005)
    
    return start_lat, start_lon