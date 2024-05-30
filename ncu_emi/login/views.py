from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from .models import User  

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
