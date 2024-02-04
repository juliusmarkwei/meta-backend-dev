from django.contrib import admin
from .models import Books, Category

admin.site.register(Books)
admin.site.register(Category)