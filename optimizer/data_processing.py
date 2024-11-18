import csv

from django.conf import settings

from .utils import estimate_travel_time, haversine


def read_csv(file_path):
    """
    Reads the CSV file and returns the content as a list of dictionaries.
    
    Args:
        file_path (str): The path to the CSV file.
    
    Returns:
        list: A list of dictionaries where each dictionary represents a row from the CSV.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def process_data(data):
    """
    Processes the CSV data to calculate distances and travel times for each route.

    Args:
        data (list): A list of dictionaries where each dictionary represents a row
                     from the CSV file, containing pickup and dropoff information.

    Returns:
        list: A list of dictionaries where each dictionary contains processed data,
              including pickup, dropoff details, distance, travel time, and a map link.
    """
    locations = []  # List to store the processed location data

    # Iterate through each row in the data to process it
    for row in data:
        # Extract pickup and dropoff coordinates as tuples
        pickup = (float(row['pickup_lat']), float(row['pickup_lng']))
        dropoff = (float(row['dropoff_lat']), float(row['dropoff_lng']))
        
        # Calculate the distance between the pickup and dropoff points using haversine formula
        distance = haversine(*pickup, *dropoff)
        
        # Estimate the travel time based on the calculated distance
        travel_time = estimate_travel_time(distance)

        # Append the processed information to the locations list
        locations.append({
            'pickup': row['pickup_address_line_1'],  # Pickup address
            'dropoff': row['dropoff_address_line_1'],  # Dropoff address
            'pickup_time_from': row['pickup_time_from'],  # Pickup time window (from)
            'pickup_time_to': row['pickup_time_to'],  # Pickup time window (to)
            'dropoff_time_from': row['dropoff_time_from'],  # Dropoff time window (from)
            'dropoff_time_to': row['dropoff_time_to'],  # Dropoff time window (to)
            'pickup_lat': pickup[0],  # Pickup latitude
            'pickup_lng': pickup[1],  # Pickup longitude
            'dropoff_lat': dropoff[0],  # Dropoff latitude
            'dropoff_lng': dropoff[1],  # Dropoff longitude
            'distance': distance,  # Calculated distance between pickup and dropoff
            'travel_time': travel_time,  # Estimated travel time for the route
            'map_link': f"{settings.GOOGLE_MAP_LINK}{pickup[0]},{pickup[1]}/{dropoff[0]},{dropoff[1]}"  # Google Maps link for the route
        })
        save_locations_to_csv(locations, f'{settings.OUTPUT_ROUTES_CSV_FILE_NAME}')

    return locations  # Return the list of processed locations with all relevant details

def save_locations_to_csv(locations, output_file='processed_locations.csv'):
    """
    Saves the processed locations to a CSV file.

    Args:
        locations (list): List of processed location data to be saved.
        output_file (str): Path to the output CSV file.
    """
    fieldnames = [
        'pickup', 'dropoff', 'pickup_time_from', 'pickup_time_to', 'dropoff_time_from',
        'dropoff_time_to', 'pickup_lat', 'pickup_lng', 'dropoff_lat', 'dropoff_lng',
        'distance', 'travel_time', 'map_link'
    ]
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write location data
        for location in locations:
            writer.writerow(location)
