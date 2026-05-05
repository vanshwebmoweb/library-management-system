from rest_framework import serializers
from library.models import Author


class AuthorListSerializer(serializers.ModelSerializer):
    total_books = serializers.IntegerField()
    total_copies = serializers.IntegerField()
    name_with_count = serializers.CharField()
    books = serializers.StringRelatedField(many = True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'bio', 'total_books', 'total_copies', 'name_with_count', 'books',)
        read_only_fields = ('id', 'total_books', 'total_copies', 'name_with_count', 'books',)


class AuthorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'bio',)

    def validate(self, data):
        name = data.get('name', '').strip()
        bio = data.get('bio')

        if name:
            if any(char.isdigit() for char in name):
                raise serializers.ValidationError({"name_contain_characters": "Author name cannot contain numbers."})

            if len(name) < 2:
                raise serializers.ValidationError({"name_too_short": "Author name must be at least 2 characters."})

        if bio:
            if len(bio) < 10:
                raise serializers.ValidationError({"bio_length": "Bio must be at least 10 characters."})

        return data


class AuthorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'bio',)

    def validate(self, data):
        name = data.get('name', '').strip()
        bio = data.get('bio')

        if name:
            if any(char.isdigit() for char in name):
                raise serializers.ValidationError({"name_contain_characters": "Author name cannot contain numbers."})

            if len(name) < 2:
                raise serializers.ValidationError({"name_too_short": "Author name must be at least 2 characters."})

        if bio:
            if len(bio) < 10:
                raise serializers.ValidationError({"bio_length": "Bio must be at least 10 characters."})

        return data


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    total_books = serializers.IntegerField()
    total_copies = serializers.IntegerField()
    name_with_count = serializers.CharField()
    books = serializers.StringRelatedField(many = True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'bio', 'total_books', 'total_copies', 'name_with_count', 'books',)
        read_only_fields = ('id', 'total_books', 'total_copies', 'name_with_count', 'books',)


class AuthorDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name',)
        read_only_fields = ('id', 'name',)