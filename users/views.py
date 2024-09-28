from rest_framework.decorators import api_view,  permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from .serializers import UserSerializer, ProfileSerializer
from .models import Profile
from rest_framework import viewsets, mixins
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError



@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            # Create user using create_user to automatically handle password hashing
            user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                email=request.data.get('email', '')
            )
            
            # Create a Profile for the user
            profile = Profile.objects.create(user=user)
            profile.save()

            # Generate a token for the new user
            token = Token.objects.create(user=user)
                     
            # Serialize the created user and return token
            serialized_user = UserSerializer(user)
            return Response({"token": token.key, "user": serialized_user.data}, status=status.HTTP_201_CREATED)
        
        # Catch the IntegrityError if username or email is not unique
        except IntegrityError:
            return Response({"error": "Username or email already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def log_in(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    login(request, user)
    user.save()

    
    # Get or create a token for the user
    token, created = Token.objects.get_or_create(user=user)

    serializer = UserSerializer(user)
   
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)




# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     # Return a structured JSON response
#     return Response({"message": f"Token valid for user {request.user.email}"})




@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def log_out(request):
    if request.method == 'POST' or request.method == 'GET':
        try:
            # Delete all tokens for the authenticated user (optional: logout from all devices)
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow update only if the profile belongs to the logged-in user
        return obj.user == request.user

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # Retrieve profile by username instead of the default id
    def get_object(self):
        username = self.kwargs.get("pk")  # `pk` is the default argument captured by routers
        profile = get_object_or_404(Profile, user__username=username)
        return profile

    # Override permissions depending on the action
    def get_permissions(self):
        # Allow any authenticated user to retrieve profiles
        if self.action in ['retrieve', 'list']:
            permission_classes = [AllowAny]
        # Only the owner can update or delete their profile
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner]
        # For any other action, just authenticated users can access
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # Handle the profile retrieve logic (read-only)
    # def retrieve(self, request, *args, **kwargs):
    #     profile = self.get_object()
    #     serializer = ProfileSerializer(profile)
    #     return Response(serializer.data)

    # # Handle profile update logic (owner-only)
    # def update(self, request, *args, **kwargs):
    #     profile = self.get_object()
    #     self.check_object_permissions(request, profile)  # Check ownership before updating
    #     return super().update(request, *args, **kwargs)