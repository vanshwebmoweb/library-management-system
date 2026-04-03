from rest_framework import serializers
from library.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)

    def validate(self, data):
        name = data.get('name')

        if name:
            if name.isdigit():
                raise serializers.ValidationError({"name": "Category name cannot be numbers only."})
            if len(name) < 3:
                raise serializers.ValidationError({"name": "Category name must be at least 3 characters."})

        return data