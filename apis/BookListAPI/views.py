from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Books, Category
from .serializers import BooksSerializer, CategorySerializer
from django.shortcuts import get_object_or_404



@api_view(['GET', 'POST'])
def books(request):
    books = Books.objects.select_related('category').all()
    serializer = BooksSerializer(books, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
def singlebook(request, id):
    book = get_object_or_404(Books, pk=id)
    serializer = BooksSerializer(book, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
def category_detail(request, id):
    category = get_object_or_404(Category, pk=id)
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

class BookList(APIView):
    def get(self, request):
        author = request.GET.get('author', None)
        return Response({'message': 'list all the books by ' + str(author)}, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response({'message': 'add a new book'}, status=status.HTTP_201_CREATED)
    
