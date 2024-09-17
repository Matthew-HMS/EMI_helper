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
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .serializers import UserSerializer, LoginSerializer  


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
            'message': '用戶註冊成功',
            'user_id': user.user_id
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        user_account = request.data.get('user_account')
        user_pw = request.data.get('user_pw')

        user = User.objects.filter(user_account=user_account).first()

        if user and user.check_password(user_pw):
            # 手動設置 session
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.user_name

            return JsonResponse({'message': '登入成功', 'user_id': user.user_id})
        else:
            return JsonResponse({'error': '帳號或密碼錯誤'}, status=400)

# class LoginView(GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         data = request.data
#         user_account = data.get('user_account')
#         user_pw = data.get('user_pw')

#         user = User.objects.filter(user_account=user_account).first()

#         if user and user.check_password(user_pw):
         
#             access_token = self.generate_jwt_token(user)
            
           
#             user.last_login = now()
#             user.save()

#             return Response({
#                 'access': access_token,

#                 'user_id': user.user_id  
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': '帳號或密碼錯誤'}, status=status.HTTP_400_BAD_REQUEST)

#     def generate_jwt_token(self, user):
#         expiration = datetime.utcnow() + timedelta(minutes=60)
#         token = jwt.encode({
#             'user_id': user.user_id,
#             'exp': expiration
#         }, settings.SECRET_KEY, algorithm='HS256')
#         return token

class UpdateView(APIView):
    def post(self, request):
        # 檢查 session 是否存在
        if 'user_id' not in request.session:
            return JsonResponse({'error': '未登入'}, status=401)

        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)

        data = request.data
        old_pw = data.get('old_pw')
        new_pw = data.get('new_pw')

        # 檢查舊密碼是否正確
        if not user.check_password(old_pw):
            return JsonResponse({'error': '舊密碼錯誤'}, status=400)

        # 如果舊密碼正確，則設置新密碼
        if new_pw:
            user.set_password(new_pw)
            user.save()
            return JsonResponse({'message': '密碼更新成功'}, status=200)

        return JsonResponse({'error': '新密碼不能為空'}, status=400)

