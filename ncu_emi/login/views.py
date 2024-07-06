from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer, LoginSerializer  


def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        user_pw = request.POST['password']
        # 使用你的自定義 User 模型來驗證用戶
        user = User.objects.filter(user_name=user_name, user_pw=user_pw).first()
        print(f'User: {user}')  
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/index/')
        else:
            messages.error(request, '帳號或密碼錯誤')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(user_account=request.data['user_account'])
        refresh = RefreshToken.for_user(user)
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)
        return response

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_account = serializer.validated_data['user_account']
        user_pw = serializer.validated_data['user_pw']
        
        user = User.objects.filter(user_account=user_account).first()
        
        if user and check_password(user_pw, user.user_pw):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.user_id,
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist() 
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
