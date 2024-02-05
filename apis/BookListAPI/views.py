from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Books, Category
from .serializers import BooksSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


@api_view(['GET', 'POST'])
def books(request):
    if request.method == 'GET':
        books = Books.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        
        if category_name:
            books = books.filter(category__name=category_name)
        if to_price:
            books = books.filter(price__lte=to_price)
            
        if search:
            books = books.filter(title__icontains=search)
        
        # ordring by multiple fields
        if ordering:
            ordering_fileds = ordering.split(',')
            books = books.order_by(*ordering_fileds)
            
        paginator = Paginator(books, per_page=perpage)
        try:
            books = paginator.page(number=page)
        except EmptyPage:
            books = []    
            
        serializer = BooksSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def singlebook(request, id):
    if request.method == 'GET':
        book = get_object_or_404(Books, pk=id)
        serializer = BooksSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        book = get_object_or_404(Books, pk=id)
        serializer = BooksSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def category_detail(request, id):
    category = get_object_or_404(Category, pk=id)
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message': 'Some secret message'}, status=status.HTTP_200_OK)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({'message': 'successful'}, status=status.HTTP_200_OK)

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({'message': 'Message for the logged in users only'}, status=status.HTTP_200_OK)

class BookList(APIView):
    def get(self, request):
        author = request.GET.get('author', None)
        return Response({'message': 'list all the books by ' + str(author)}, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response({'message': 'add a new book'}, status=status.HTTP_201_CREATED)
    
