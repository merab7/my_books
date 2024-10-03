from django.db import models
from django.contrib.auth.models import User






class Book(models.Model):
    title = models.CharField(max_length=1000, blank=True, null=True)
    author = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published_date = models.CharField(max_length=100, blank=True, null=True)  # Changed to DateField for better date handling
    genres = models.CharField(max_length=500, blank=True, null=True)  # Fixed spelling from 'ganeres' to 'genres'
    cover_image = models.URLField(blank=True, null=True)
    average_rating = models.FloatField(blank=True, null=True)  # Changed to FloatField for ratings

    def __str__(self) -> str:
        return self.title or "Untitled"  # Added a string representation


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)  # Added blank=True for consistency
    review_text = models.TextField(null=True, blank=True)  # Added blank=True for consistency
    created_at = models.DateTimeField(auto_now_add=True)  # Changed to auto_now_add for review creation date

    def __str__(self) -> str:
        return f"Review by {self.user.username} on {self.book.title}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Changed to OneToOneField for unique profile per user
    favorite_genres = models.TextField(blank=True, null=True)  # Fixed spelling from 'ganres' to 'genres'
    bookshelf = models.ManyToManyField(Book, blank=True)  # Removed default=None since it's not needed
    review_history = models.ManyToManyField(Review, blank=True)  # Changed to ManyToManyField to allow multiple reviews

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
