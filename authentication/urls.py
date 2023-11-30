from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('ask_reset_password', views.AskResetPwdView.as_view(), name='ask_reset_password'),
    path('reset_password/<int:uid>/<token>', views.ResetPwdView.as_view(), name='reset_password')
]