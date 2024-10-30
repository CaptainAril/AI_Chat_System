import json

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Chat, User
from .serializers import ChatSerializer, UserLoginSerializer, UserSerializer
from .utilities import chat_response


# Create your views here.
class UserView(APIView):
    permission_classes = [AllowAny]    
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            user = User.objects.get(pk=serializer.data['username'])
            data = {
                'username':serializer.data.get('username'),
                'token':user.tokens
            }
            return Response({"status": "successs", "message":"User Account created", 'data':data}, status=status.HTTP_201_CREATED)
        return Response({"status": "An Error occured", "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(data={'message' : 'All Users retrieved', 'status': 'success', 'data':UserSerializer(User.objects.all(), many=True).data})


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    # serializer_class = UserLoginSerializer
    
    def post(self, request):
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            
            # Authenticate the user
            user = authenticate(request=request, username=username, password=password)
            if user:
                response = super().post(request=request)
                
                data = {
                    'status': '200',
                    'message': 'Login succesfull',
                    'username': user.username,
                    'access': response.data.get('access'),
                    'refresh': response.data.get('refresh')
                    }
                
                return Response(data=data, status=status.HTTP_200_OK)
            
            return Response({'status': '401', 'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({"status": "An Error occured", "Errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(data={'status':'success', 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
            except (TokenError, InvalidToken):
                return Response({"status": "error", "message": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "message": "Refresh token required for logout."}, status=status.HTTP_400_BAD_REQUEST)
    
    
class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        chats = Chat.objects.filter(user=request.user)
        serializer = ChatSerializer(chats, many=True)
        data = {
            'user_account': request.user.username,
            'chats': serializer.data
        }
        return Response(data={'status': "success", 'message' : 'Chats retrieved', **data})
        
    
    def post(self, request):
        if request.user.tokens < 100:
                return Response({'status': 'error', 'message': 'Insufficient tokens'}, status=status.HTTP_402_PAYMENT_REQUIRED)
            
        data = request.data.copy()
        data['user'] = request.user
        serializer = ChatSerializer(data=data)
    
        if serializer.is_valid():
            serializer.save()

            request.user.tokens -= 100
            request.user.save()
            
            data = {
            'user_account': request.user.username,
            'chat': serializer.data
        }
            
            return Response(data={'status': 'success', 'message' : 'New chat record', **data}, status=status.HTTP_201_CREATED)

        return Response({"status": "error", "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class TokenBalanceView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_authenticated:
            data = {
                'username': request.user.username,
                'token_balance': request.user.tokens
            }
            return Response({'status':'success', 'message': 'Token balance', **data}, status=status.HTTP_200_OK)
        return Response({'status':'error', 'message': 'Login Required!'}, status=status.HTTP_401_UNAUTHORIZED)