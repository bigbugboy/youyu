from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    return redirect('expense')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('expense/', include('expense.urls')),
    path('authentication/', include('authentication.urls')),
]
