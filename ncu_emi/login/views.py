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

import json


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data['last_login'] = datetime.now()
        data['is_active'] = 0

        if User.objects.filter(user_account=data['user_account']).exists():
            return JsonResponse({
                'error': '用戶帳號已存在，請選擇其他帳號'
            }, status=status.HTTP_400_BAD_REQUEST)
        
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

class UpdateView(GenericAPIView):
    
    serilizer_user = UserSerializer

    def get_queryset(self):
        # 假設你要從 User 模型中取得資料
        return User.objects.all()

    def get(self, request):
        user_id = request.GET.get('user_id')
        
        if user_id:
            print("gpt get by user")
            user_instance = self.get_queryset().filter(user_id=user_id)
        else:
            # 如果沒有 user_id，可能要返回一些默認資料
            user_instance = self.get_queryset()
       
        serializer = self.serilizer_user(user_instance, many=True)
        data = serializer.data
        return JsonResponse(
            json.loads(json.dumps(data, ensure_ascii=False)),
            status=status.HTTP_200_OK,
            safe=False
        )

    def post(self, request):
        # 檢查 session 是否存在
        # if 'user_id' not in request.session:
        #     return JsonResponse({'error': '未登入'}, status=401)

        # user_id = request.session['user_id']
        # user_account = request.GET.get('user_account')
        data = request.data
        user_id = data.get('user_id')
        print("user_id: ",user_id)
        user = User.objects.get(user_id=user_id)
 
        
        user_old_pw = data.get('user_old_pw')
        user_new_pw = data.get('user_new_pw')
        new_user_account = data.get('user_account')
        new_user_name = data.get('user_name')

        if new_user_name:
            print("change user name")
            user.user_name = new_user_name    

        if new_user_account:
            if User.objects.filter(user_account=new_user_account).exclude(user_id=user_id).exists():
                return JsonResponse({'message': '用戶帳號已存在，請選擇其他帳號'}, status=400)
            print("change user account")
            user.user_account = new_user_account
        
        if user_old_pw and user_new_pw :
            # 檢查舊密碼是否正確
            if not user.check_password(user_old_pw):
                print('舊密碼錯誤')
                return JsonResponse({'message': '舊密碼錯誤'}, status=400)
            # 如果舊密碼正確，則設置新密碼      
            user.set_password(user_new_pw)
            user.save()
            print('密碼更新成功')
            return JsonResponse({'message': '密碼更新成功'}, status=200)     
        elif user_old_pw and not user_new_pw :
            return JsonResponse({'message': '密碼不能為空'}, status=400)
        elif not user_old_pw and user_new_pw :
            return JsonResponse({'message': '密碼不能為空'}, status=400)
        else:
            return JsonResponse({'message': '帳號更新成功'}, status=200)
            

