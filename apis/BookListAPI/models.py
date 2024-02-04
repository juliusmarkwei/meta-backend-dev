from django.db import models
import uuid

class Category(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Categories'
        

class Books(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    published_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, default=None)
    
    def __str__(self) -> str:
        return f'{str(self.author)} - {str(self.title)}'
    
    class Meta:
        verbose_name_plural = 'Books'