from rest_framework import serializers
from .models import Books, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        
        
class BooksSerializer(serializers.ModelSerializer):
    contributor = serializers.SerializerMethodField(method_name='get_contributor')
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Books
        fields = ['id', 'author', 'title', 'price', 'published_date', 'contributor', 'category']
        depth = 1
        
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Price must be greater than 0')
        
    def get_contributor(self, obj: Books):
        return 'John Doe'
    