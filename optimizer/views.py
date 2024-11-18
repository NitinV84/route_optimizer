import os
import csv
from django.http import JsonResponse
from django.shortcuts import render
from django.http import Http404
from .optimize_routes import optimize_routes
from .data_processing import read_csv, process_data
from django.conf import settings

# View to optimize routes based on CSV data
def optimize_routes_view(request):
    """
    View to optimize routes for delivery or travel based on a CSV file.
    The CSV file contains customer requests with pickup and dropoff information.
    
    Returns:
        JsonResponse: A response containing optimized routes with map links.
    """
    file_path = os.path.join('data', f'{settings.CSV_FILE_NAME}')

    if os.path.exists(file_path):
        # Read and process the CSV data
        data = read_csv(file_path)
        locations = process_data(data)

        # Optimize routes based on processed data
        optimized_routes = optimize_routes(locations)

        # Extract the map links for the optimized routes
        map_links = [route['map_link'] for route in optimized_routes]
        
        # Return only the map links in the JSON response
        return JsonResponse({"optimized_routes": map_links})
    else:
        # Return an error response if the file is not found
        return JsonResponse({"error": "File not found."}, status=404)


# Data source view for displaying raw CSV data
def data_source_table_view(request):
    """
    View to display the raw data from the CSV file in a tabular format.

    Returns:
        Rendered HTML page with the CSV data.
    """
    file_path = os.path.join('data', 'customer-requests-testingLondon36.csv')
    data = []

    if os.path.exists(file_path):
        # Open and read the CSV file
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)

    # Render the data in the 'optimizer/data_source.html' template
    return render(request, 'optimizer/data_source.html', {"data": data})


# View for displaying the route data from the optimized CSV file
def route_data_view(request):
    """
    View to display the route data from the optimized routes CSV file.

    The route data includes information like pickup, dropoff, time, distance, 
    travel time, and map links for each optimized route.

    Returns:
        Rendered HTML page with the route data.
    """
    # Path to the optimized routes CSV file
    file_path = f'{settings.OUTPUT_ROUTES_CSV_FILE_NAME}'

    route_data = []

    try:
        # Open the optimized routes CSV file and read the data
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)  # Read the CSV as dictionaries
            for row in reader:
                # Append each row to the route_data list
                route_data.append({
                    'pickup': row['pickup'],
                    'dropoff': row['dropoff'],
                    'pickup_time_from': row['pickup_time_from'],
                    'pickup_time_to': row['pickup_time_to'],
                    'dropoff_time_from': row['dropoff_time_from'],
                    'dropoff_time_to': row['dropoff_time_to'],
                    'distance': float(row['distance']),
                    'travel_time': float(row['travel_time']),
                    'map_link': row['map_link']
                })
    except FileNotFoundError:
        # Raise a 404 error if the file is not found
        raise Http404("CSV file not found")

    # Return the rendered template with the route data
    return render(request, 'optimizer/links.html', {'route_data': route_data})
