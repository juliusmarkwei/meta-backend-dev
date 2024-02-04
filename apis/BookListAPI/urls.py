from django.urls import path
from .views import books, BookList, singlebook, category_detail

urlpatterns = [
    path('books', books, name='books'),
    path('books/<int:id>', singlebook, name='singlebook'),
    path('category/<int:id>', category_detail, name='category-detail'),
]