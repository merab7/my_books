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
        fields= ['title', 'author', 'description', ' published_date', 'ganeres', 'cover_image', 'avarage_rating']


class ReviewSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    book = BookSerializer()
    
    class Meta:
        model = Review
        fields = ['user', 'book', 'rating', 'review_text', 'created_at']




class ProfileSerializer(serializers.ModelSerializer):
     
    user = UserSerializer()
    bookshelf = BookSerializer(many=True)
    review_history = ReviewSerializer()

    class Meta(object):
        model = Profile
        fields = ['user', 'favorite_ganres', 'bookshelf', 'review_history']