from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    throttle_classes
)
from rest_framework import status
from django.contrib.auth.models import User
from .models import (
    MenuItem
)
from django.core.exceptions import ObjectDoesNotExist
from .serializers import MenuItemSerializer


@api_view(['GET', 'POST'])
def menu_item(request):
    if request.method == 'GET':
        menuItems = MenuItem.objects.all()
        return Response(menuItems, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        if request.user.groups.filter(name='Manager').exists():
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def menu_item_detail(request, menuItem):
    try:
        menuItem_obj = MenuItem.objects.get(pk=menuItem)
    except MenuItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MenuItemSerializer(menuItem_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.user.groups.filter(name='Manager').exists():
        if request.method in ['PUT', 'PATCH']:
            serializer = MenuItemSerializer(menuItem_obj, data=request.data, partial=request.method == 'PATCH')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'DELETE':
            menuItem_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_403_FORBIDDEN)
