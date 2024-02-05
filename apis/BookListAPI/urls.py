from django.urls import path
from .views import books, BookList, singlebook, category_detail, secret, throttle_check, throttle_check_auth
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('books', books, name='books'),
    path('books/<int:id>', singlebook, name='singlebook'),
    path('category/<int:id>', category_detail, name='category-detail'),
    path('secret', secret, name='secret'),
    path('obtain-auth-token/', obtain_auth_token, name='obtain_auth_token'),
    path('throttle-check', throttle_check, name='throttle-check'),
    path('throttle_check_auth', throttle_check_auth, name='throttle_check_auth'),
]