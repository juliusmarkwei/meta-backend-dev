from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView


@api_view(['GET', 'POST'])
def books(request):
    return Response("Books", status=status.HTTP_200_OK)

class BookList(APIView):
    def get(self, request):
        author = request.GET.get('author', None)
        return Response({'message': 'list all the books by ' + author}, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response({'message': 'add a new book'}, status=status.HTTP_201_CREATED)