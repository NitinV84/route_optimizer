from django.urls import path
from .views import optimize_routes_view, data_source_table_view, route_data_view

urlpatterns = [
    path('optimize-route/', optimize_routes_view, name="optimize_route"),
    path('data-source/', data_source_table_view, name="data_source_table"),
    path('route-data-view/', route_data_view, name="route_data")
]
