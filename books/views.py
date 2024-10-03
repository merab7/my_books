from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import environ
import json




@api_view(['POST', 'GET'])
def search_for_book(request):
    # Get parameters from the POST body
    title = request.data.get('title')
    author = request.data.get('author')

    env = environ.Env()
    environ.Env.read_env()


    API_KEY = env('BOOK_API')


    r =  requests.get(f'https://www.googleapis.com/books/v1/volumes?q={title}+inauthor:{author}&key={API_KEY}')


    data = r.json()
    
    print(json.dumps(data, indent=4,  ensure_ascii=False))
    
    searched_books = [
        {
            'title': x['volumeInfo'].get('title', 'Unknown Title'),
            'author': x['volumeInfo'].get('authors', ['Unknown Author']),
            'description': x['volumeInfo'].get('description', ['Unknown Description']),
            'published_date': x['volumeInfo'].get('publishedDate', 'Unknown Date'),
            'genres': x['volumeInfo'].get('categories', ['Unknown Genre']),
            'cover_image_url': x['volumeInfo'].get('imageLinks', {}).get('thumbnail', 'No Image Available')
        } 
        for x in data.get('items', [])
    ]
    print(searched_books)
 

# Handle missing parameters
    if not title and not author:
        return Response({"error": "Please provide at least a 'title' or 'author' parameter."}, 
                        status=status.HTTP_400_BAD_REQUEST)

    # Simulate search result or API call here
    return Response(searched_books)




