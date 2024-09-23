from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=1000, blank=True, null=True)
    author = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField( blank=True, null=True)
    published_date = models.CharField(max_length=100, blank=True, null=True)
    ganeres = models.CharField(max_length=500, blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    avarage_rating = models.CharField(max_length=20, blank=True, null=True)



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(null=True)
    review_text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True) 




class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    favorite_ganres = models.TextField(null=True, blank=True)
    bookshelf = models.ManyToManyField(Book, blank=True)
    review_history = models.ForeignKey(Review, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"



