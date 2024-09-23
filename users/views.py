from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        # Create user using create_user to automatically handle password hashing
        user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            email=request.data.get('email', '')
        )
        token = Token.objects.create(user=user)
        
        # Serialize the created user and return token
        serialized_user = UserSerializer(user)
        return Response({"token": token.key, "user": serialized_user.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def log_in(request):
    user = get_object_or_404(User, username=request.data['username'])
    
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    # Get or create a token for the user
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    # Return a structured JSON response
    return Response({"message": f"Token valid for user {request.user.email}"})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def log_out(request):
    # Get the token object for the authenticated user
    try:
        token = Token.objects.get(user=request.user)
        # Delete the token, effectively logging the user out
        token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token or user already logged out."}, status=status.HTTP_400_BAD_REQUEST)