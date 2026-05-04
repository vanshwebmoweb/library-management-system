from rest_framework import serializers
from library.models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

    def validate(self, data):
        name = data.get('name')
        if name:
            if name.isdigit():
                raise serializers.ValidationError({"name_contain_characters": "Category name cannot be numbers only."})
            if len(name) < 3:
                raise serializers.ValidationError({"name_length": "Category name must be at least 3 characters."})
        return data


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

    def validate(self, data):
        name = data.get('name')
        if name:
            if name.isdigit():
                raise serializers.ValidationError({"name_contain_characters": "Category name cannot be numbers only."})
            if len(name) < 3:
                raise serializers.ValidationError({"name_length": "Category name must be at least 3 characters."})
        return data


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategoryDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id', 'name',)