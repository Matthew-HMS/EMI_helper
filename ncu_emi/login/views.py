from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout

import jwt
from datetime import datetime, timedelta
from django.conf import settings
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

        return JsonResponse({
            'message': '註冊成功',
            'user_id': user.user_id
        }, status=status.HTTP_201_CREATED)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        user_account = data.get('user_account')
        user_pw = data.get('user_pw')

        user = User.objects.filter(user_account=user_account).first()

        if user :
            print("test1")
        if user.check_password(user_pw):
            print("test2")

        if user and user.check_password(user_pw):
         
            access_token = self.generate_jwt_token(user)
            
           
            user.last_login = now()
            user.save()

            return Response({
                'access': access_token,

                'user_id': user.user_id  
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': '帳號或密碼錯誤'}, status=status.HTTP_400_BAD_REQUEST)

    def generate_jwt_token(self, user):
        expiration = datetime.utcnow() + timedelta(minutes=60)
        token = jwt.encode({
            'user_id': user.user_id,
            'exp': expiration
        }, settings.SECRET_KEY, algorithm='HS256')
        return token


# class LogoutView(APIView):
#     def post(self, request):
#         auth_header = request.headers.get('Authorization')
#         if auth_header and auth_header.startswith('Bearer '):
#             access_token = auth_header.split(' ')[1]
#             try:
#                 jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])

#                 TokenBlacklist.objects.create(token=access_token)
#                 return Response({'message': '登出成功，令牌已加入黑名單'}, status=status.HTTP_200_OK)
#             except jwt.ExpiredSignatureError:
#                 return Response({'error': '令牌已過期'}, status=status.HTTP_400_BAD_REQUEST)
#             except jwt.InvalidTokenError:
#                 return Response({'error': '無效令牌'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'error': '未提供令牌'}, status=status.HTTP_400_BAD_REQUEST)
    
