from rest_framework import serializers
from .models import Books, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        
        
class BooksSerializer(serializers.ModelSerializer):
    contributor = serializers.SerializerMethodField(method_name='get_contributor')
    category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name='category-detail',
        lookup_field = 'pk'
    )
    class Meta:
        model = Books
        fields = ['id', 'author', 'title', 'published_date', 'contributor', 'category']
        depth = 1
        
    def get_contributor(self, obj: Books):
        return 'John Doe'
    