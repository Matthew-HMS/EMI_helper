from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.db import transaction
from django.http import JsonResponse
from django.utils.timezone import now

from .models import User
from .serializers import UserSerializer, LoginSerializer  



# def index_view(request):
#     return render(request, 'index.html')

# def login_view(request):
#     if request.method == 'POST':
#         user_name = request.POST['username']
#         user_pw = request.POST['password']
#         # 使用你的自定義 User 模型來驗證用戶
#         user = User.objects.filter(user_name=user_name, user_pw=user_pw).first()
#         print(f'User: {user}')  
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect('/index/')
#         else:
#             messages.error(request, '帳號或密碼錯誤')
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')


    


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data['last_login'] = datetime.now()
        data['is_active'] = 0
        
        user = User(
            user_account=data['user_account'],
            user_name=data['user_name'],
            user_pw=data['user_pw'],
            is_active=data['is_active'],
            last_login=data['last_login']
        )
        
        user.set_password(data['user_pw']) 
        user.save()

        return JsonResponse({'message': '用戶註冊成功'}, status=status.HTTP_201_CREATED)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        user_account = data.get('user_account')
        user_pw = data.get('user_pw')

        user = User.objects.filter(user_account=user_account).first()

        if user and user.check_password(user_pw):
            refresh = RefreshToken.for_user(user)
            user.last_login = datetime.now()
            user.save()

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.user_id
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': '帳號或密碼錯誤'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': '登出成功，令牌已失效'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
