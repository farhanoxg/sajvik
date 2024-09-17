from django.urls import path
from .views import get_filtered_colleges , get_filtered_options

urlpatterns = [
    path('filtered-colleges/', get_filtered_colleges, name='filtered-colleges'),
     path('filtered-options/', get_filtered_options, name='filtered-options'),
]
