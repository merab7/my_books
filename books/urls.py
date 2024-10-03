from django.urls import path
from .views import search_for_book

urlpatterns = [
     path('search/', search_for_book, name='search'),
]