import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from email_validator import validate_email, EmailNotValidError

from .forms import RegisterForm
from . import models


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


def validate_username(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        if not username.strip():
            return JsonResponse({'status': 'error', 'msg': '用户名不能为空'}, status=400)
        if User.objects.filter(username=username.strip()).exists():
            return JsonResponse({'status': 'error', 'msg': '用户名已存在'}, status=400)
        else:
            return JsonResponse({'status': 'success', 'msg': 'OK'})


class ValidateEmailView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not email.strip():
            return JsonResponse({'status': 'error', 'msg': '邮箱不能为空'}, status=400)
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as e:
            return JsonResponse({'status': 'error', 'msg': '邮箱格式错误'}, status=400)
        if User.objects.filter(username=email.strip()).exists():
            return JsonResponse({'status': 'error', 'msg': '邮箱已存在'}, status=400)
        else:
            return JsonResponse({'status': 'success', 'msg': 'OK'})


class ChangePasswordView(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        return render(request, 'authentication/change_password.html')
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        old_password = request.POST.get('old-password')
        if not request.user.check_password(old_password):
            messages.error(request, '旧密码验证错误')
            return render(request, 'authentication/change_password.html')
        
        new_password = request.POST.get('new-password')
        re_password = request.POST.get('re-password')
        if len(new_password) < 6:
            messages.error(request, '新密码不能少于6位')
            return render(request, 'authentication/change_password.html')
        if new_password != re_password:
            messages.error(request, '新密码两次输入不一致')
            return render(request, 'authentication/change_password.html')
        
        request.user.set_password(new_password)
        request.user.save()     # 切记不要忘记save
        messages.success(request, '密码修改成功')
        return render(request, 'authentication/change_password.html')


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(login_required(login_url='login'), name='post')
class UploadAvatar(View):

    def get(self, request):
        print(111)
        
        return render(request, 'authentication/upload_avatar.html')
    
    def post(self, request):
        # 演示使用FileField
        userinfo, _ = models.UserInfo.objects.update_or_create(
            user=request.user, 
            defaults={'avatar': request.FILES.get('avatar')}
        )
        messages.success(request, '上传成功')
        return render(request, 'authentication/upload_avatar.html')    



@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(login_required(login_url='login'), name='post')
class UploadAvatarBinary(View):
    def get(self, request):
        return render(request, 'authentication/upload_avatar.html')
    
    def post(self, request: HttpRequest):
        # 演示使用BinaryField
        from io import BytesIO
        bio = BytesIO()
        for chunk in request.FILES.get('avatar').chunks():
            bio.write(chunk)

        models.UserInfo.objects.update_or_create(
            user=request.user, 
            defaults={'avatarBinary': bio.getvalue()}
        )
        messages.success(request, '上传成功')
        return render(request, 'authentication/upload_avatar.html')
