from django.contrib import admin
from .models import Book, Review, Profile

admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Review)