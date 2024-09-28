from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Book, Review



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class BookSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Book
        fields= ['title', 'author', 'description', 'published_date', 'genres', 'cover_image', 'average_rating']


class ReviewSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    book = BookSerializer()
    
    class Meta:
        model = Review
        fields = ['user', 'book', 'rating', 'review_text', 'created_at']




class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    bookshelf = BookSerializer(many=True, read_only=True)
    review_history = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'favorite_genres', 'bookshelf', 'review_history']