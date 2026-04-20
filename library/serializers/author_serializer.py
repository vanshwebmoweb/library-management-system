from rest_framework import serializers
from library.models import Author



class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True)
    total_books = serializers.IntegerField()

    class Meta:
        model = Author
        fields = ('id', 'name', 'bio', 'books', 'total_books',)
        read_only_fields = ('id', 'books', 'total_books',)

    def validate(self, data):
        name = data.get('name', '').strip()
        bio = data.get('bio')

        if name:
            if any(char.isdigit() for char in name):
                raise serializers.ValidationError({"name_contain_characters": "Author name cannot contain numbers."})
            if len(name) < 2:
                raise serializers.ValidationError({"name_too_short": "Author name must be at least 2 characters."})
        else:
            raise serializers.ValidationError({"name_rules": "Author name is required and must be at least 2 characters."})

        if bio:
            if len(bio) < 10:
                raise serializers.ValidationError({"bio_length": "Bio must be at least 10 characters."})

        return data