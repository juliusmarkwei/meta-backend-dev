from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.menu_item, name='menu_item'),
    path('menu-items/<int:menuItem>', views.menu_item_detail, name='menu_item_detail'),
    
]