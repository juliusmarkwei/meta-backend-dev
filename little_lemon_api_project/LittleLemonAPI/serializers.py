from rest_framework import serializers
from .models import MenuItem 

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']
        read_only_fields = ['id']

    def validate(self, data):
        required_fields = ['title', 'price', 'featured', 'category']
        
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({field: 'This field is required'})
        
        if data['price'] < 0:
            raise serializers.ValidationError({'price': 'Price cannot be negative'})
        return data