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
    MenuItem,
)
from django.core.exceptions import ObjectDoesNotExist
from .serializers import MenuItemSerializer, CartSerializer


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


@api_view(['GET', 'POST'])
def manage_managers_group(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            managers = User.objects.filter(groups__name='Manager')
            return Response(managers, status=status.HTTP_200_OK)
        if request.method == 'POST':
            try:
                manager = User.objects.get(pk=request.data['manager'])
                manager.groups.add(1)
                return Response(status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
def remove_manager(request, userId):
    if request.user.groups.filter(name='Manager').exists():
        try:
            manager_obj = User.objects.get(pk=userId)
            manager_group = Group.objects.get(name='Manager')
            manager_obj.groups.remove(manager_group)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
def manage_delivery_crew_group(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            deliveryCrew = User.objects.filter(groups__name='Delivery Crew')
            return Response(deliveryCrew, status=status.HTTP_200_OK)
        if request.method == 'POST':
            try:
                deliveryCrew = User.objects.get(pk=request.data['deliveryCrew'])
                deliveryCrew_group = Group.objects.get(name='Manager')
                deliveryCrew.groups.add(deliveryCrew_group)
                return Response(status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
def remove_delivery_crew(request, userId):
    if request.user.groups.filter(name='Manager').exists():
        try:
            deliveryCrew_obj = User.objects.get(pk=userId)
            deliveryCrew_group = Group.objects.get(name='Delivery Crew')
            deliveryCrew_obj.groups.remove(deliveryCrew_group)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST', 'DELETE'])
def cart_menu_item(request):
    if request.method == 'GET':
        try:
            cartItems = Cart.objects.filter(user=request.user)
            many = cartItems.count() > 1
            serializer = CartSerializer(cartItems, many=many)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        try:
            cartItems = Cart.objects.filter(user=request.user)
            cartItems.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)