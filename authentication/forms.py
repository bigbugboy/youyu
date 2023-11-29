from typing import Any
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(
        min_length=6, max_length=100, 
        error_messages={
        'min_length': '密码不能少于6位',
        'max_length': '密码不能超多100位',
        'required': '密码不能为空',
    })
    re_password = forms.CharField(min_length=6, max_length=100)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error('username', '用户名已存在')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', '邮箱已占用')
        return email
    
    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            self.add_error('re_password', '两次密码输入不一致')
        return self.cleaned_data
