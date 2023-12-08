from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('ask_reset_password', views.AskResetPwdView.as_view(), name='ask_reset_password'),
    path('reset_password/<int:uid>/<token>', views.ResetPwdView.as_view(), name='reset_password'),
    path('validate-username', views.validate_username, name='validate-username'),
    path('validate-email', csrf_exempt(views.ValidateEmailView.as_view()), name='validate-email'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('upload-avatar', views.UploadAvatar.as_view(), name='upload-avatar'),
    path('upload-avatar-binary', views.UploadAvatarBinary.as_view(), name='upload-avatar-binary'),
    
]