from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'refresh': str(refresh),  # Send the refresh token
            'access': str(refresh.access_token),  # Send the access token
        }, status=200)
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['GET'])
def get_user_details(request):
    if request.user.is_authenticated:
        return Response({
            "username": request.user.username,
        })
    return Response({'error': 'Unauthorized'}, status=401)