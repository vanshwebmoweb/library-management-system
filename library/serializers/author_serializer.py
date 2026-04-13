from rest_framework import serializers
from library.models import Author



class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True, read_only=True)
    total_books = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'bio', 'books', 'total_books',)

    def validate(self, data):
        name = data.get('name', '').strip()
        bio = data.get('bio')

        if name:
            if any(char.isdigit() for char in name):
                raise serializers.ValidationError({"name": "Author name cannot contain numbers."})
            if len(name) < 2:
                raise serializers.ValidationError({"name": "Author name must be at least 2 characters."})
        else:
            raise serializers.ValidationError({"name": "Author name is required and must be at least 2 characters."})

        if bio:
            if len(bio) < 10:
                raise serializers.ValidationError({"bio": "Bio must be at least 10 characters."})

        return data