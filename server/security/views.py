from django.contrib.auth import authenticate, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from security.models import Profile
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        user_profile = Profile.objects.get(user=user)
        return Response({'token': token.key, 'user': str(user)})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Logged out successfully'})
    except Token.DoesNotExist:
        return Response({'error': 'No token found'}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username_view(request, pk):
    user_profile = Profile.objects.get(user=request.user)
    return Response({'user': str(user_profile.user.username)})


