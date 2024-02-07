from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    throttle_classes,
)
from rest_framework import status
from django.contrib.auth.models import User
from .models import (
    MenuItem,
)
from django.core.exceptions import ObjectDoesNotExist
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle


@api_view(['GET', 'POST'])
def menu_item(request):
    if request.method == 'GET':
        menuItems = MenuItem.objects.all()
        
        # Filtering
        category = request.query_params.get('category', None)
        if category is not None:
            menuItems = menuItems.filter(category=category)
        many = menuItems.count() > 1
        
        # Pagination
        paginator = PageNumberPagination()
        paginated_menuItems = paginator.paginate_queryset(menuItems, request)
        
        serializer = MenuItemSerializer(paginated_menuItems, many=many)
        return paginator.get_paginated_response(serializer.data)
    
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
        

@api_view(['GET', 'POST'])
@throttle_classes([UserRateThrottle])
def order(request):
    if request.method == 'GET':
        try:
            orders = Order.objects.filter(user=request.user)
            many = orders.count() > 1
            serializer = OrderSerializer(orders, many=many)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Get cart items for the current user
            cart_items = Cart.objects.filter(user=request.user)
            
            # Add cart items to the order items table
            for cart_item in cart_items:
                order_item = OrderItem.objects.create(
                    order=serializer.instance,
                    menu_item=cart_item.menu_item,
                    quantity=cart_item.quantity
                )
                order_item.save()
            
            # Delete all items from the cart for this user
            cart_items.delete()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def order_detail(request, orderId):
    try:
        order = Order.objects.get(pk=orderId)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'PUT' and request.user.groups.filter(name='Manager').exists():
        delivery_crew_id = request.data.get('deliveryCrewId')
        status = request.data.get('status')
        
        if delivery_crew_id is not None:
            try:
                delivery_crew = User.objects.get(pk=delivery_crew_id)
                order.delivery_crew = delivery_crew
            except User.DoesNotExist:
                return Response({'error': 'Invalid delivery crew ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        if status is not None:
            if status == 0 or status == 1:
                order.status = status
            else:
                return Response({'error': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.save()
        return Response({'message': 'Order updated successfully'}, status=status.HTTP_200_OK)
    
    if request.method in ['PUT', 'PATCH']:
        serializer = OrderSerializer(order, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
