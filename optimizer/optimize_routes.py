import csv
import os
import time
from datetime import timedelta
from math import atan2, cos, radians, sin, sqrt

import pandas as pd
from django.conf import settings


def optimize_routes(locations, distance_limit=120, time_limit=480):
    """
    Optimizes a set of delivery or travel routes based on distance and time constraints.

    Args:
        locations (list): A list of dictionaries, each representing a location with its 
                           distance and travel time details.
        distance_limit (float): The maximum allowable distance (in kilometers) for the route.
        time_limit (int): The maximum allowable time (in minutes) for the route (default is 8 hours).

    Returns:
        list: A list of dictionaries containing optimized route map links.
    """
    
    # Initialize variables for route optimization
    optimized_routes = []  # List to store the optimized routes
    current_time = 0  # Start with 0 minutes for total time
    total_distance = 0  # Start with 0 km for total distance
    route = []  # List to hold the route locations

    # Iterate through the locations and build the optimized route
    for location in locations:
        # Check if adding this location exceeds the distance limit
        if total_distance + location['distance'] > distance_limit:
            break  # Stop if the route exceeds the distance limit
        
        # Check if adding this location exceeds the time limit
        if current_time + location['travel_time'] > time_limit:
            break  # Stop if the route exceeds the time limit
        
        # Add the location to the route
        route.append(location)
        total_distance += location['distance']  # Add the location's distance to total distance
        current_time += location['travel_time']  # Add the location's travel time to total time

    # Generate Google Maps links for each location in the optimized route
    for loc in route:
        # Format the map link for the route from pickup to dropoff location
        route_map_link = f"{settings.GOOGLE_MAP_LINK}{loc['pickup_lat']},{loc['pickup_lng']}/{loc['dropoff_lat']},{loc['dropoff_lng']}"
        
        # Add the map link to the list of optimized routes
        optimized_routes.append({
            'map_link': route_map_link  # Store the map link for this location
        })

    # Return the list of optimized route map links
    return optimized_routes
