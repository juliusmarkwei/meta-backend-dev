from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.menu_item, name='menu_item'),
    path('menu-items/<int:menuItem>', views.menu_item_detail, name='menu_item_detail'),
    path('groups/manager/users', views.manage_managers_group, name='manage_managers_group'),
    path('groups/manager/users/<int:userId>', views.remove_manager, name='remove_manager'),
    path('groups/delivery-crew/users', views.manage_delivery_crew_group, name='manage_delivery_crew_group'),
    path('groups/delivery-crew/users/<int:userId>', views.remove_delivery_crew, name='remove_delivery_crew'),
    path('cart/menu-items', views.cart_menu_item, name='cart_menu_item'),
]