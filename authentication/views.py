from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator

from .forms import RegisterForm


def register(request):
    if request.method == 'GET':
        return render(request, 'authentication/register.html')
    else:
        form_obj = RegisterForm(request.POST)
        if form_obj.is_valid():
            print(form_obj.cleaned_data)
            user = User(
                username=form_obj.cleaned_data['username'],
                email=form_obj.cleaned_data['email'],
            )
            user.set_password(form_obj.cleaned_data['password'])
            user.is_active = True   # TODO: VERIFY ACCOUNT
            user.save()
            return redirect(to='login')
        else:
            context = {
                'values': request.POST,
                'form_obj': form_obj,
            }
            return render(request, 'authentication/register.html', context)


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        context = {'values': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request, '用户名不存在')
            return render(request, 'authentication/login.html', context)
        
        user = User.objects.get(username=username)
        if not user.check_password(password):
            messages.error(request, '密码错误')
            return render(request, 'authentication/login.html', context)
        else:
            auth.login(request, user)
            messages.success(request, '登录成功')
            return redirect(to='expense')


def logout(request):
    auth.logout(request)
    messages.success(request, '退出成功')
    return redirect(to='login')


class AskResetPwdView(View):
    def get(self, request):
        return render(request, 'authentication/ask_reset_password.html')
    
    def post(self, request):
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            context = {
                'error': '邮箱不存在',
                'email': email
            }
            return render(request, 'authentication/ask_reset_password.html', context)
        
        # todo: send the reset-password link to user by email
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        # todo: uid and link
        link = f'http://127.0.0.1:9090/authentication/reset_password/{user.pk}/{token}'
        print('link', link)
        messages.success(request, '重置密码邮件已发您邮箱, 请查收')
        messages.success(request, link)
        return redirect(to='login')



class ResetPwdView(View):

    def _get_user_and_check_token(self, uid, token):
        user = get_object_or_404(User, pk=uid)
        if not default_token_generator.check_token(user, token):
            return HttpResponseBadRequest('Invalid token')
        return user

    def get(self, request, uid, token):
        user = self._get_user_and_check_token(uid, token)
        messages.info(request, f'Hello {user.username}, 请输入新密码')
        return render(request, 'authentication/reset_password.html')
    
    def post(self, request, uid, token):
        user = self._get_user_and_check_token(uid, token)
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if password != re_password:
            messages.error(request, '两次密码输入不一致')
            return render(request, 'authentication/reset_password.html')

        user.set_password(password)
        user.save()
        messages.success(request, '密码修改成功，请使用新密码登录')
        return redirect('login')
    