from django.urls import path
from .views import display_even_numbers

urlpatterns = [
    path('numbers/', display_even_numbers),
]
