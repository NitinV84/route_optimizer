import math


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two points on Earth using the Haversine formula.
    
    The Haversine formula calculates the great-circle distance between two points
    given their longitude and latitude in degrees.

    Args:
        lat1 (float): Latitude of the first point in decimal degrees.
        lon1 (float): Longitude of the first point in decimal degrees.
        lat2 (float): Latitude of the second point in decimal degrees.
        lon2 (float): Longitude of the second point in decimal degrees.
    
    Returns:
        float: The distance between the two points in kilometers.
    """
    R = 6371  # Radius of the Earth in kilometers
    phi1 = math.radians(lat1)  # Convert latitude from degrees to radians
    phi2 = math.radians(lat2)  # Convert latitude from degrees to radians
    delta_phi = math.radians(lat2 - lat1)  # Difference in latitudes (radians)
    delta_lambda = math.radians(lon2 - lon1)  # Difference in longitudes (radians)

    # Haversine formula to calculate the distance
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in kilometers


def estimate_travel_time(distance):
    """
    Estimates the travel time based on the distance using a constant average speed.
    
    This function assumes an average speed of 50 km/h to calculate travel time.

    Args:
        distance (float): The distance to be traveled in kilometers.
    
    Returns:
        float: The estimated travel time in minutes.
    """
    average_speed = 50  # Assume an average speed of 50 km/h
    return (distance / average_speed) * 60  # Convert travel time to minutes
